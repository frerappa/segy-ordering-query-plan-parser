import argparse
import pathlib
from src.simple.parser import QPParser
from src.simple.semantic import SemanticVisitor
from src.simple.qp_ast import *
from src.utils.node_visitor import *


class TranslationVisitor(NodeVisitor):
    def __init__(self):
        self.table_name = "Table"

    def visit_Program(self, node: Program):
        filter_text = ""
        order_text = ""
        for step in node.steps:
            self.visit(step)
            if isinstance(step, Filter):
                filter_text = step.text
            elif isinstance(step, Order):
                order_text = step.text
        node.text: str = f"SELECT * FROM {self.table_name} {filter_text} {order_text} ;"


    def visit_EmptyStatement(self, node: EmptyStatement):
        pass

    def visit_UnaryOp(self, node: UnaryOp):
        self.visit(node.expr)

        operator_map = {
            "not": "NOT",
            "+": "+",
            "-": "-"
        }

        node.text = f"({operator_map[node.op]} {node.expr.text})"


    def visit_BinaryOp(self, node: BinaryOp):
        self.visit(node.lvalue)
        self.visit(node.rvalue)

        operator_map = {
            "<": "<",
            "<=": "<=",
            ">": ">",
            ">=": ">=",
            "=": "=",
            "!=": "<>",
            "and": "AND",
            "or": "OR",
        }

        node.text = f"({node.lvalue.text} {operator_map[node.op]} {node.rvalue.text})"


    def visit_ID(self, node: ID):
        node.text = node.name

    def visit_Constant(self, node: Constant):
        node.text = node.value

    def visit_Order(self, node: Order):
        order = ""
        for i, expression in enumerate(node.orderings):
            self.visit(expression)
            order += f"{expression.text}"
            if i != len(node.orderings) - 1:
                order += " , "
        node.text = f"ORDER BY {order}"


    def visit_Filter(self, node: Filter):
        self.visit(node.expression)
        node.text = f"WHERE {node.expression.text}"


if __name__ == "__main__":
    # create argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_file", help="Path to file to be translated to SQL", type=str
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
        visitor = SemanticVisitor()
        visitor.visit(ast)
        translator = TranslationVisitor()
        translator.visit(ast)
        print(ast.text)
