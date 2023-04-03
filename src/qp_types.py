class Type:
    """
    Class that represents a type in the uC language.  Basic
    Types are declared as singleton instances of this type.
    """

    def __init__(
            self, name, binary_ops=set(), unary_ops=set(), rel_ops=set(), assign_ops=set()
    ):
        self.typename = name
        self.unary_ops = unary_ops
        self.binary_ops = binary_ops
        self.rel_ops = rel_ops

    def __str__(self):
        return "type({})".format(self.typename)


NumberType = Type(
    "number",
    unary_ops={"-", "+"},
    binary_ops=set(),
    rel_ops={"=", "!=", "<", ">", "<=", ">="},
)

CharType = Type(
    "char",
    unary_ops=set(),
    binary_ops=set(),
    rel_ops={"=", "!="},
)

StringType = Type(
    "string",
    unary_ops=set(),
    binary_ops=set(),
    rel_ops={"=", "!="},
)


BooleanType = Type(
    "bool",
    unary_ops={"not"},
    binary_ops={"and", "or"},
    rel_ops={"=", "!="},
)

