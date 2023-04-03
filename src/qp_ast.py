from abc import ABC
from abc import abstractmethod

import sys


def represent_node(obj, indent):
    def _repr(obj, indent, printed_set):
        """
        Get the representation of an object, with dedicated pprint-like format for lists.
        """
        if isinstance(obj, list):
            indent += 1
            sep = ",\n" + (" " * indent)
            final_sep = ",\n" + (" " * (indent - 1))
            return (
                "["
                + (sep.join((_repr(e, indent, printed_set) for e in obj)))
                + final_sep
                + "]"
            )
        elif isinstance(obj, Node):
            if obj in printed_set:
                return ""
            else:
                printed_set.add(obj)
            result = obj.__class__.__name__ + "("
            indent += len(obj.__class__.__name__) + 1
            attrs = []

            # convert each node attribute to string
            for name, value in vars(obj).items():

                # is an irrelevant attribute: skip it.
                if name in ('bind', 'coord'):
                    continue

                # relevant attribte not set: skip it.
                if value is None:
                    continue

                # relevant attribute set: append string representation.
                value_str = _repr(value, indent + len(name) + 1, printed_set)
                attrs.append(name + "=" + value_str)

            sep = ",\n" + (" " * indent)
            final_sep = ",\n" + (" " * (indent - 1))
            result += sep.join(attrs)
            result += ")"
            return result
        elif isinstance(obj, str):
            return obj
        else:
            return str(obj)

    # avoid infinite recursion with printed_set
    printed_set = set()
    return _repr(obj, indent, printed_set)


#
# ABSTRACT NODES
#
class Node(ABC):
    """Abstract base class for AST nodes."""

    attr_names = ()

    @abstractmethod
    def __init__(self, coord=None):
        self.coord = coord

    def __repr__(self):
        """Generates a python representation of the current node"""
        return represent_node(self, 0)

    def children(self):
        """A sequence of all children that are Nodes"""
        pass

    def show(
        self,
        buf=sys.stdout,
        offset=0,
        attrnames=False,
        nodenames=False,
        showcoord=False,
        _my_node_name=None,
    ):
        """Pretty print the Node and all its attributes and children (recursively) to a buffer.
        buf:
            Open IO buffer into which the Node is printed.
        offset:
            Initial offset (amount of leading spaces)
        attrnames:
            True if you want to see the attribute names in name=value pairs. False to only see the values.
        nodenames:
            True if you want to see the actual node names within their parents.
        showcoord:
            Do you want the coordinates of each Node to be displayed.
        """
        lead = " " * offset
        if nodenames and _my_node_name is not None:
            buf.write(lead + self.__class__.__name__ + " <" + _my_node_name + ">: ")
            inner_offset = len(self.__class__.__name__ + " <" + _my_node_name + ">: ")
        else:
            buf.write(lead + self.__class__.__name__ + ":")
            inner_offset = len(self.__class__.__name__ + ":")

        if self.attr_names:
            if attrnames:
                nvlist = [
                    (n, represent_node(getattr(self, n), offset+inner_offset+1+len(n)+1))
                    for n in self.attr_names
                    if getattr(self, n) is not None
                ]
                attrstr = ", ".join("%s=%s" % nv for nv in nvlist)
            else:
                vlist = [getattr(self, n) for n in self.attr_names]
                attrstr = ", ".join(
                    represent_node(v, offset + inner_offset + 1) for v in vlist
                )
            buf.write(" " + attrstr)

        if showcoord:
            if self.coord and self.coord.line != 0:
                buf.write(" %s" % self.coord)
        buf.write("\n")

        for (child_name, child) in self.children():
            child.show(buf, offset + 4, attrnames, nodenames, showcoord, child_name)


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