import sys
import argparse
import pathlib
from sly import Parser
from lexer import QPLexer
from coord import Coord
from src.qp_ast import *


class QPParser(Parser):
    tokens = QPLexer.tokens

    precedence = (
        ('left', 'COMMA'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'EQ', 'NE'),
        ('left', 'LT', 'LE', 'GT', 'GE'),
        ('left', 'PLUS', 'MINUS'),
        ('right', 'NOT'),
    )

    start = 'program'

    debugfile = 'parser.out'

    def __init__(self, debug=True):
        self.lex = QPLexer(self._lexer_error)
        self.lex.build()

        # Keeps track of the last token given to yacc (the lookahead token)
        self._last_yielded_token = None

    def parse_text(self, text: str):
        return self.parse(self.lex.tokenize(text))

    def _lexer_error(self, msg, line, column):
        # use stdout to match with the output in the .out test files
        print("LexerError: %s at %d:%d" % (msg, line, column), file=sys.stdout)
        sys.exit(1)

    def _parser_error(self, msg, coord=None):
        # use stdout to match with the output in the .out test files
        if coord is None:
            print("ParserError: %s" % (msg), file=sys.stdout)
        else:
            print("ParserError: %s %s" % (msg, coord), file=sys.stdout)
        sys.exit(1)

    def _token_coord(self, p):
        return Coord(p.lineno, self.lex.find_tok_column(p))

    @_('filter order',
       'order filter')
    def program(self, p):
        steps = [p.filter, p.order]
        return Program(steps, p[0].coord)

    @_('filter',
       'order')
    def program(self, p):
        steps = [p[0]]
        return Program(steps, p[0].coord)

    @_('empty')
    def program(self, p):
        return Program([])

    @_('')
    def empty(self, p):
        pass

    @_('ORDER COLON id_list SEMI')
    def order(self, p):
        return Order(p.id_list, self._token_coord(p))

    @_('FILTER COLON expression SEMI')
    def filter(self, p):
        return Filter(p.expression, self._token_coord(p))

    @_('id')
    def id_list(self, p):
        return [p.id]

    @_('id_list COMMA id')
    def id_list(self, p):
        return p.id_list + [p.id]

    @_('ID')
    def id(self, p):
        return ID(p.ID, self._token_coord(p))

    @_('INT_CONST',
       'REAL_CONST')
    def constant(self, p):
        return Constant('number', p[0], self._token_coord(p))

    @_('STRING_LITERAL')
    def constant(self, p):
        return Constant('string', p[0], self._token_coord(p))

    @_('CHAR_CONST')
    def constant(self, p):
        return Constant('char', p[0], self._token_coord(p))

    @_('TRUE',
       'FALSE')
    def constant(self, p):
        return Constant('bool', p[0], self._token_coord(p))

    @_('unary_expression')
    def expression(self, p):
        return p.unary_expression

    @_('expression LT expression',
       'expression LE expression',
       'expression GT expression',
       'expression GE expression',
       'expression EQ expression',
       'expression NE expression',
       'expression AND expression',
       'expression OR expression')
    def expression(self, p):
        return BinaryOp(op=p[1].lower(), left=p.expression0, right=p.expression1, coord=self._token_coord(p))

    @_('primary_expression')
    def unary_expression(self, p):
        return p.primary_expression

    @_('PLUS unary_expression',
       'MINUS unary_expression',
       'NOT unary_expression', )
    def unary_expression(self, p):
        return UnaryOp(p[0].lower(), p.unary_expression, self._token_coord(p))


    @_('id',
       'constant')
    def primary_expression(self, p):
        return p[0]

    @_('LPAREN expression RPAREN')
    def primary_expression(self, p):
        return p.expression

    def error(self, p):
        if p:
            self._parser_error(
                "Before %s" % p.value, Coord(p.lineno, self.lex.find_tok_column(p))
            )
        else:
            self._parser_error("At the end of input (%s)" % self.lex.filename)


if __name__ == "__main__":

    # create argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Path to file to be parsed", type=str)
    args = parser.parse_args()

    # get input path
    input_file = args.input_file
    input_path = pathlib.Path(input_file)

    # check if file exists
    if not input_path.exists():
        print("ERROR: Input", input_path, "not found", file=sys.stderr)
        sys.exit(1)


    def print_error(msg, x, y):
        print("Lexical error: %s at %d:%d" % (msg, x, y), file=sys.stderr)


    # set error function
    p = QPParser()
    l = QPLexer(p._lexer_error)
    # open file and print ast
    with open(input_path) as f:
        ast = p.parse_text(f.read())
        ast.show(buf=sys.stdout, showcoord=True)
