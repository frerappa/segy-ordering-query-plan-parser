from src.utils.node import Node
class Constant(Node):

    attr_names = ('type', 'value')

    def __init__(self, type, value, coord=None):
        """
        I create an instance of this class.

        :param type: primitive type.
        :param value: constant value.
        :param coord: code position.
        """
        self.type = type
        self.value = value
        self.coord = coord

    def children(self):
        return ()


class EmptyStatement(Node):

    attr_names = ()

    def __init__(self, coord=None):
        self.coord = coord

    def children(self):
        return ()


class ID(Node):

    attr_names = ("name",)

    def __init__(self, name, coord=None):
        """
        I create an instance of this class.

        :param name: ID unique name.
        :param coord: code position.
        """
        self.name = name
        self.coord = coord

    def children(self):
        return ()


class Program(Node):

    attr_names = ()

    def __init__(self, steps=list[Node], coord=None):
        self.steps = steps
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.steps or []):
            nodelist.append(("steps[%d]" % i, child))
        return tuple(nodelist)


class Operation(Node):
    attr_names = ("op",)

    def __init__(self, op, coord=None):
        """
        I create an instance of this class.

        :param op: unary operator (!, +, -, ...)
        """
        self.op = op
        self.coord = coord

    def children(self):
        nodelist = []
        return tuple(nodelist)


class UnaryOp(Operation):

    attr_names = ("op",)

    def __init__(self, op, expr, coord=None):
        """
        I create an instance of this class.

        :param op: unary operator (!, +, -, ...)
        :param expr: expression whose value will be modified by the operator.
        """
        self.op = op
        self.expr = expr
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expr is not None:
            nodelist.append(("expr", self.expr))
        return tuple(nodelist)


class BinaryOp(Operation):

    attr_names = ("op",)

    def __init__(self, op, left, right, coord=None):
        """
        I create an instance of this class.

        :param op: binary operator (+, -, *, ...).
        :param left: left hand side expression.
        :param right: right hand side expression.
        :param coord: code position.
        """
        self.op = op
        self.lvalue = left
        self.rvalue = right
        self.coord = coord

    def children(self):
        nodelist = []
        if self.lvalue is not None:
            nodelist.append(("lvalue", self.lvalue))
        if self.rvalue is not None:
            nodelist.append(("rvalue", self.rvalue))
        return tuple(nodelist)


class Order(Node):

    attr_names = ()

    def __init__(self, orderings: list[ID], coord=None):
        self.orderings = orderings
        self.coord = coord

    def children(self):
        nodelist = []
        for i, child in enumerate(self.orderings or []):
            nodelist.append(("orderings[%d]" % i, child))
        return tuple(nodelist)


class Filter(Node):

    attr_names = ()

    def __init__(self, expression: Operation, coord=None):
        self.expression = expression
        self.coord = coord

    def children(self):
        nodelist = []
        if self.expression is not None:
            nodelist.append(("expr", self.expression))
        return tuple(nodelist)