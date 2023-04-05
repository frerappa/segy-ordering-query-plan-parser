import argparse
import pathlib
from copy import deepcopy
from typing import Any, Dict, Union
from parser import QPParser
from src.qp_types import *
from coord import Coord
from src.qp_ast import *
from node_visitor import *

class Visitor(NodeVisitor):
    def __init__(self):
        self.typemap: Dict[str, Type] = {
            "number": NumberType,
            "char": CharType,
            "bool": BooleanType,
            "string": StringType
        }

    def _assert_semantic(self, condition: bool, msg_code: int, coord, name: str = "", ltype: str = "", rtype: str = ""):
        """Check condition, if false print selected error message and exit"""
        error_msgs = {
            1: f"Filter statement must contain a boolean expression, not {name}",
            2: "Order expression must contain identifiers",
            3: f"Binary operator {name} does not have matching LHS/RHS types - {ltype} and {rtype}",
            4: f"Binary operator {name} is not supported by {ltype}",
            5: f"Unary operator {name} is not supported by {ltype}",
        }
        if not condition:
            msg = error_msgs[msg_code]  # invalid msg_code raises Exception
            print("Semantic error: %s %s" % (msg, coord), file=sys.stdout)
            sys.exit(1)

    def visit_Program(self, node: Program):
        for step in node.steps:
            self.visit(step)

    def visit_EmptyStatement(self, node: EmptyStatement):
        pass

    def visit_UnaryOp(self, node: UnaryOp):
        self.visit(node.expr)

        expression_type = node.expr.type
        self._assert_semantic(
            node.op in expression_type.unary_ops,
            5,
            coord=node.coord,
            name=node.op,
            ltype=expression_type
        )

        node.type: Type = expression_type

    def visit_BinaryOp(self, node: BinaryOp):
        self.visit(node.lvalue)
        self.visit(node.rvalue)

        left_type, right_type = node.lvalue.type, node.rvalue.type

        if not (isinstance(node.lvalue, ID) or isinstance(node.rvalue, ID)):
            self._assert_semantic(
                left_type == right_type,
                3,
                coord=node.coord,
                name=node.op,
                ltype=left_type,
                rtype=right_type
            )

            self._assert_semantic(
                node.op in left_type.rel_ops or node.op in left_type.binary_ops,
                4,
                coord=node.coord,
                name=node.op,
                ltype=left_type
            )

        node.type = BooleanType

    def visit_ID(self, node: ID):
        node.type: Type = NumberType
        pass

    def visit_Constant(self, node: Constant):
        node.type: Type = self.typemap[node.type]

    def visit_Order(self, node: Order):
        for expression in node.orderings:
            self.visit(expression)

            self._assert_semantic(
                isinstance(expression, ID),
                2,
                expression.coord
            )

    def visit_Filter(self, node: Filter):
        self.visit(node.expression)

        self._assert_semantic(
            node.expression.type == BooleanType,
            1,
            node.expression.coord
        )


if __name__ == "__main__":
    # create argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_file", help="Path to file to be semantically checked", type=str
    )
    args = parser.parse_args()

    # get input path
    input_file = args.input_file
    input_path = pathlib.Path(input_file)

    # check if file exists
    if not input_path.exists():
        print("Input", input_path, "not found", file=sys.stderr)
        sys.exit(1)

    # set error function
    p = QPParser()
    # open file and parse it
    with open(input_path) as f:
        ast = p.parse_text(f.read())
        sema = Visitor()
        sema.visit(ast)
