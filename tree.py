import ast
from dataclasses import dataclass
from lexer import IntToken, FloatToken, StringToken

# Abstract Syntax Tree classes
class AST:
    pass

@dataclass
class BinOp(AST):
    op: str
    left: AST
    right: AST

@dataclass
class Number(AST):
    val: IntToken | FloatToken | StringToken

@dataclass
class If(AST):
    c: AST
    t: AST
    e: AST

# Evaluator function
def evaluate_ast(tree: AST):
    """
    Evaluates a custom AST using Python's ast module and handles custom tokens.
    """
    match tree:
        case Number(val):
            return val
        case BinOp(op, left, right):
            left_val = evaluate_ast(left)
            right_val = evaluate_ast(right)

            if isinstance(left_val, (IntToken, FloatToken)) and isinstance(right_val, (IntToken, FloatToken)):
                # Numeric operations
                left_value = left_val.value
                right_value = right_val.value

                if isinstance(left_val, FloatToken) or isinstance(right_val, FloatToken):
                    result = eval_math(op, float(left_value), float(right_value))
                    return FloatToken(result)
                result = eval_math(op, int(left_value), int(right_value))
                return IntToken(result)

            elif isinstance(left_val, StringToken) and isinstance(right_val, StringToken):
                # String concatenation
                if op == "+":
                    return StringToken(left_val.value + right_val.value)
                raise TypeError(f"Unsupported operation: {op} for strings")

            elif isinstance(left_val, StringToken) and isinstance(right_val, IntToken):
                # String repetition
                if op == "*":
                    return StringToken(left_val.value * right_val.value)
                raise TypeError(f"Unsupported operation: {op} for string and int")
            
            else:
                raise TypeError(f"Incompatible types: {type(left_val).__name__} and {type(right_val).__name__}")

        case If(c, t, e):
            cond = evaluate_ast(c)
            if isinstance(cond, BoolToken) and cond.value:
                return evaluate_ast(t)
            return evaluate_ast(e)
        case _:
            raise ValueError("Unknown AST node")

def eval_math(op: str, left: float, right: float) -> float:
    """
    Uses Python's ast module to safely evaluate mathematical operations.
    """
    # Define a mapping for operators
    allowed_ops = {
        "+": ast.Add,
        "-": ast.Sub,
        "*": ast.Mult,
        "/": ast.Div,
        "^": ast.Pow,
    }
    if op not in allowed_ops:
        raise ValueError(f"Unsupported operator: {op}")
    # Create an AST node and evaluate it
    operation = allowed_ops[op]()
    binop_node = ast.BinOp(
        left=ast.Constant(left), op=operation, right=ast.Constant(right)
    )
    return eval(compile(ast.Expression(binop_node), filename="<ast>", mode="eval"))
