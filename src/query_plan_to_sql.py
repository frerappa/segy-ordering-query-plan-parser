import sys
import argparse

from src.lexer import QPLexer
from src.parser import QPParser
from src.semantic import SemanticVisitor
from src.translate import TranslationVisitor


class QueryPlanToSQL:
    def translate(self, query_plan: str) -> str:
        lexer = QPLexer()
        parser = QPParser(lexer)
        semantic_visitor = SemanticVisitor()
        translation_visitor = TranslationVisitor()

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

    args = parser.parse_args()
    query_plan = args.query_plan
    if args.input_file:
        f = open(args.input_file)
        query_plan = f.read()

    if not query_plan:
        print("Missing query plan")
        sys.exit(1)
    translation = qptsql.translate(query_plan)
    if not translation:
        print()
    if args.output_file:
        f = open(args.output_file, 'w')
        f.write(translation)
    if args.print_result:
        print(translation)
