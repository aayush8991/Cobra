from lark import Lark, Transformer, v_args
from lexer import IntToken, FloatToken, StringToken, OperatorToken
from ast_class import AST, BinOp, Number

# Grammar definition for parsing arithmetic expressions
grammar = """
    ?start: expr
    ?expr: term
         | expr "+" term   -> add
         | expr "-" term   -> sub
    ?term: factor
         | term "*" factor -> mul
         | term "/" factor -> div
    ?factor: atom
           | factor "^" atom -> pow
    ?atom: NUMBER           -> number
         | "(" expr ")"
    %import common.NUMBER
    %import common.WS_INLINE
    %ignore WS_INLINE
"""

# Define the parser using Lark
parser = Lark(grammar, parser='lalr', transformer=None)

# Transformer to convert parse tree into an AST
class ASTTransformer(Transformer):
    @v_args(inline=True)
    def add(self, left, right):
        return BinOp('+', left, right)

    def sub(self, left, right):
        return BinOp('-', left, right)

    def mul(self, left, right):
        return BinOp('*', left, right)

    def div(self, left, right):
        return BinOp('/', left, right)

    def pow(self, left, right):
        return BinOp('^', left, right)

    def number(self, value):
        if '.' in value:  # Handle FloatToken
            return Number(FloatToken(float(value)))
        return Number(IntToken(int(value)))  # Handle IntToken

# Parse function using Lark and the transformer
def parse(expression):
    tree = parser.parse(expression)
    return ASTTransformer().transform(tree)
