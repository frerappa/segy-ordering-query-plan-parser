import argparse
import pathlib
import sys
from sly import Lexer


class QPLexer(Lexer):
    def __init__(self, error_func):
        """Create a new Lexer.
        An error function. Will be called with an error
        message, line and column as arguments, in case of
        an error during lexing.
        """
        self.error_func = error_func
        self.filename = ""

        # Keeps track of the last token returned from self.token()
        self.last_token = None

    def build(self, **kwargs):
        return

    def reset_lineno(self):
        """Resets the internal line number counter of the lexer."""
        self.lineno = 1

    def find_tok_column(self, token):
        """Find the column of the token in its line."""
        last_cr = self.text.rfind('\n', 0, token.index)
        if last_cr < 0:
            last_cr = 0
        return token.index - last_cr

    # Internal auxiliary methods
    def _error(self, msg, token):
        location = self._make_tok_location(token)
        self.error_func(msg, location[0], location[1])
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

        # Delimeters
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
    def unterminatedcomment(self, t):
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


    def print_error(msg, x, y):
        # use stdout to match with the output in the .out test files
        print("Lexical error: %s at %d:%d" % (msg, x, y), file=sys.stdout)


    # set error function
    m = QPLexer(print_error)
    # Build the lexer
    m.build()
    # open file and print tokens
    with open(input_path) as f:
        m.scan(f.read())