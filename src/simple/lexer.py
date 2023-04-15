import argparse
import pathlib
import sys
from sly import Lexer


class QPLexer(Lexer):
    def __init__(self):
        self._found_error = False

    def _print_error(self, msg: str, x: int, y: int):
        print("Lexical error: %s @ %d:%d" % (msg, x, y), file=sys.stdout)

    def find_tok_column(self, token):
        """Find the column of the token in its line."""
        last_cr = self.text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        return token.index - last_cr

    def _error(self, msg, token):
        self._found_error = True
        location = self._make_tok_location(token)
        self._print_error(msg, location[0], location[1])
        self.index += 1

    def _make_tok_location(self, token):
        return token.lineno, self.find_tok_column(token)

    # Reserved keywords
    keywords = (
        "FILTER",
        "ORDER",
        "OR",
        "AND",
        "NOT",
        "TRUE",
        "FALSE"
    )

    keyword_map = {
        "filter": "FILTER",
        "order": "ORDER",
        "or": "OR",
        "and": "AND",
        "not": "NOT",
        "true": "TRUE",
        "false": "FALSE"
    }
    #
    # All the tokens recognized by the lexer
    #
    tokens = set(keywords + (
        # Identifiers
        "ID",

        # constants
        "INT_CONST",
        "REAL_CONST",
        "CHAR_CONST",
        "STRING_LITERAL",

        # Operators
        "PLUS",  # +
        "MINUS",  # -

        "LT",  # <
        "LE",  # <=
        "GT",  # >
        "GE",  # >=
        "EQ",  # =
        "NE",  # !=

        # Delimiters
        "LPAREN",  # (
        "RPAREN",  # )
        "COMMA",  # ,
        "COLON",  # :
        "SEMI",  # ,
    ))

    #
    # Rules
    #
    ignore = " \t"

    # Newlines
    @_(r'\n+')
    def ignore_newlines(self, t):
        r'\n+'
        self.lineno += t.value.count('\n')

    @_(r'[a-zA-Z][0-9a-zA-Z_]*')
    def ID(self, t):
        t.type = self.keyword_map.get(t.value.lower(), "ID")
        return t

    @_(r'/\-((\-[^/])|([^(\-)]))*\-/', r'//.*')
    def comment(self, t):
        t.lineno += t.value.count("\n")

    @_('/-(.|\n)*')
    def unterminated_comment(self, t):
        msg = "Unterminated comment"
        self._error(msg, t)

    @_(r'[0-9]+[.][0-9]+')
    def REAL_CONST(self, t):
        t.value = float(t.value)
        return t

    @_(r'[0-9]+')
    def INT_CONST(self, t):
        t.value = int(t.value)
        return t

    CHAR_CONST = r'\'.\''

    @_(r'\"(\\.|[^"\\])*\"')
    def STRING_LITERAL(self, t):
        t.value = t.value.replace('"', "")
        return t

    @_(r'\'|"')
    def unmatchedquote(self, t):
        msg = "Unterminated string"
        self._error(msg, t)

    PLUS = r'\+'

    MINUS = r'-'

    NE = r'!='

    LE = r'<='

    LT = r'<'

    GE = r'>='

    GT = r'>'

    EQ = r'='

    LPAREN = r'\('

    RPAREN = r'\)'

    COMMA = r'\,'

    COLON = r'\:'

    SEMI = r'\;'

    def error(self, t):
        msg = "Illegal character %s" % repr(t.value[0])
        self._error(msg, t)

    @_(r'\'|"')
    def unmatchedquote(self, t):
        msg = "Unterminated string"
        self._error(msg, t)

    # Scanner (used only for test)
    def scan(self, data):
        output = ""
        for token in self.tokenize(data):
            print(token)
            output += str(token) + "\n"
        return output

    def tokenize(self, text, lineno=1, index=0):
        return super().tokenize(text, lineno, index)

    def has_error(self) -> bool:
        return self._found_error


if __name__ == "__main__":

    # create argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="Path to file to be scanned", type=str)
    args = parser.parse_args()

    # get input path
    input_file = args.input_file
    input_path = pathlib.Path(input_file)

    # check if file exists
    if not input_path.exists():
        print("Input", input_path, "not found", file=sys.stderr)
        sys.exit(1)


    lexer = QPLexer()
    # open file and print tokens
    with open(input_path) as f:
        lexer.scan(f.read())
