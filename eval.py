from tree import *
from lexer import *
from decimal import Decimal

def lookup(env, v, i = None):
    for u, uv in reversed(env):
        if isinstance(u, Var):
            if u.v == v and u.i == i:
                return uv
        else:
            if u == v:
                return uv
    raise ValueError("No value found.")

def e(tree: AST, stack=None):

    if stack is None:
        stack = []

    match tree:
        case Token():
            return tree
        case Var(v, i):
            return lookup(stack, v, i)
        case Fun(name, func_para, func_exp, func_body):
            stack.append((name, (func_para, func_exp)))
            x = e(func_body, stack)
            stack.pop()
            return x
        case Call(name, value):
            a, b = lookup(stack, name)
            stack.append((a, e(value, stack)))
            y = e(b, stack)
            stack.pop()
            return y
        case Let(variable, value_expr, body_expr):
            value = e(value_expr, stack)
            stack.append((variable, value))
            result = e(body_expr, stack)
            stack.pop()
            return result
        case While():
            return eval_loop(tree, stack)
        case BinOp():
            return eval_math(tree, stack)
        case If():
            return eval_cond(tree, stack)
        case _:
            raise ValueError(f"Unknown AST node := {tree}")

def eval_math(tree: BinOp, stack):
    left = e(tree.left, stack)
    right = e(tree.right, stack)

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
        case "!=":
            if isinstance(left, (IntToken, FloatToken)) and isinstance(right, (IntToken, FloatToken)):
                return BoolToken(Decimal(left.v) != Decimal(right.v))
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} == {type(right).__name__}")

def eval_cond(tree: If, stack):
    """
    Evaluate a conditional expression.
    """
    if e(tree.cond, stack).v:
        return e(tree.then, stack)
    else:
        return e(tree.else_, stack)

def eval_loop(tree: While, stack):
    while True:
        condition = e(tree.condition, stack).v
        if not (isinstance(condition, BoolToken) and condition.v):
            break
        return e(tree.body, stack)