from tree import *
from lexer import *
from decimal import Decimal

def lookup(env, v):
    for u, uv in reversed(env):
        if u == v:
            return uv
    raise ValueError("No value found.")

def e(tree: AST, env: dict[str, IntToken | FloatToken | StringToken | BoolToken] = None):
    """
    Evaluate an AST node in the given environment.
    """
    if env is None:
        env = []

    match tree:
        case Token():
            return tree
        case Var(v):
            return lookup(env, v)
        case Let(variable, value_expr, body_expr):
            value = e(value_expr, env)
            env.append((variable, value))
            result = e(body_expr, env)
            env.pop()
            return result   
        case WhileLoop(condition, body):
            return eval_loop(tree, env)
        case BinOp():
            return eval_math(tree, env)
        case If():
            return eval_cond(tree, env)
        case _:
            raise ValueError("Unknown AST node")

def eval_math(tree: BinOp, env: dict[str, IntToken | FloatToken | StringToken | BoolToken]):
    left = e(tree.left, env)
    right = e(tree.right, env)

    match tree.op:
        case "+":
            if isinstance(left, (IntToken, FloatToken)) and isinstance(right, (IntToken, FloatToken)):
                if isinstance(left, FloatToken) or isinstance(right, FloatToken):
                    return FloatToken(left.v + right.v)
                return IntToken(left.v + right.v)
            elif isinstance(left, StringToken) and isinstance(right, StringToken):
                return StringToken(left.v + right.v)
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} + {type(right).__name__}")
        case "*":
            if isinstance(left, StringToken) and isinstance(right, IntToken):
                return StringToken(left.v * int(right.v))
            elif isinstance(left, IntToken) and isinstance(right, StringToken):
                return StringToken(int(right.v) * left.v)
            elif isinstance(left, (IntToken, FloatToken)) and isinstance(right, (IntToken, FloatToken)):
                if isinstance(left, FloatToken) or isinstance(right, FloatToken):
                    return FloatToken(left.v * right.v)
                return IntToken(left.v * right.v)
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} * {type(right).__name__}")
        case "-":
            if isinstance(left, (IntToken, FloatToken)) and isinstance(right, (IntToken, FloatToken)):
                if isinstance(left, FloatToken) or isinstance(right, FloatToken):
                    return FloatToken(left.v - right.v)
                return IntToken(left.v - right.v)
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} - {type(right).__name__}")
        case "/":
            if isinstance(left, (IntToken, FloatToken)) and isinstance(right, (IntToken, FloatToken)):
                if right.v == 0:
                    raise ZeroDivisionError("Division by zero")
                return FloatToken(left.v / right.v)
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} / {type(right).__name__}")
        case "^":
            if isinstance(left, (IntToken, FloatToken)) and isinstance(right, (IntToken, FloatToken)):
                if isinstance(left, FloatToken) or isinstance(right, FloatToken):
                    return FloatToken(left.v ** right.v)
                return IntToken(left.v ** right.v)
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} ^ {type(right).__name__}")
        case ">":
            if isinstance(left, (IntToken, FloatToken)) and isinstance(right, (IntToken, FloatToken)):
                return BoolToken(Decimal(left.v) > Decimal(right.v))
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} > {type(right).__name__}")
        case "<":
            if isinstance(left, (IntToken, FloatToken)) and isinstance(right, (IntToken, FloatToken)):
                return BoolToken(Decimal(left.v) < Decimal(right.v))
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} < {type(right).__name__}")
        case "==":
            if isinstance(left, (IntToken, FloatToken)) and isinstance(right, (IntToken, FloatToken)):
                return BoolToken(Decimal(left.v) == Decimal(right.v))
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} == {type(right).__name__}")

def eval_cond(tree: If, env: dict[str, IntToken | FloatToken | StringToken | BoolToken]):
    if (e(tree.cond)).v:    # if e(tree.cond) == BoolToken(True):
        return e(tree.then)
    else:
        return e(tree.else_)

def eval_loop(tree: WhileLoop, env: dict[str, IntToken | FloatToken | StringToken | BoolToken]):
    while True:
        condition = e(tree.condition, env)
        if not (isinstance(condition, BoolToken) and condition.v):
            break
        for stmt in tree.body:
            e(stmt, env)
