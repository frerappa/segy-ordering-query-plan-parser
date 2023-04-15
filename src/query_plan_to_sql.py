import sys
import argparse

from src.simple.lexer import QPLexer
from src.simple.parser import QPParser
from src.simple.semantic import SemanticVisitor
from src.simple.translate import TranslationVisitor

from src.extended.lexer import QPLexerExtended
from src.extended.parser import QPParserExtended
from src.extended.semantic import SemanticVisitorExtended
from src.extended.translate import TranslationVisitorExtended


class QueryPlanToSQL:
    def translate(self, query_plan: str, version=2) -> str:
        if version == 1:
            lexer = QPLexer()
            parser = QPParser(lexer)
            semantic_visitor = SemanticVisitor()
            translation_visitor = TranslationVisitor()
        elif version == 2:
            lexer = QPLexerExtended()
            parser = QPParserExtended(lexer)
            semantic_visitor = SemanticVisitorExtended()
            translation_visitor = TranslationVisitorExtended()
        else:
            print("Version not supported")
            return

        tokens = lexer.tokenize(query_plan)
        if lexer.has_error():
            return
        ast = parser.parse(tokens)
        if parser.has_error():
            return
        semantic_visitor.visit(ast)
        if semantic_visitor.has_error():
            return
        translation_visitor.visit(ast)
        return ast.text


if __name__ == "__main__":
    qptsql = QueryPlanToSQL()

    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("-i", "--input-file", dest="input_file", help="Path to query plan file", default=None)
    parser.add_argument("-o", "--output-file", dest="output_file", help="Path to output file", default=None)
    parser.add_argument("-p", "--print", dest="print_result", action="store_true", help="Print resulting SQL query")
    parser.add_argument("-q", "--query-plan", dest="query_plan", default=None, help="Pass SQL as parameter")
    parser.add_argument("-v", "--version", dest="version", help="Query Plan version: 1 (simple) or 2 (extended)", default=2)


    args = parser.parse_args()
    query_plan = args.query_plan
    if args.input_file:
        f = open(args.input_file)
        query_plan = f.read()

    if not query_plan:
        print("Missing query plan")
        sys.exit(1)
    translation = qptsql.translate(query_plan, int(args.version))
    if not translation:
        print()
    else:
        if args.output_file:
            f = open(args.output_file, 'w')
            f.write(translation)
        if args.print_result:
            print(translation)
