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
        case Array(elements):
            return [e(elem, stack) for elem in elements]
        case ArrayIndex(array, index):
            arr = e(array, stack)
            idx = e(index, stack)
            if not isinstance(idx, IntToken):
                raise TypeError("Array index must be an integer")
            if not isinstance(arr, list):
                raise TypeError("Cannot index into non-array")
            if idx.v < 0 or idx.v >= len(arr):
                raise IndexError("Array index out of bounds")
            return arr[int(idx.v)]
        case ArrayAssign(array, index, value):
            arr = e(array, stack)
            idx = e(index, stack)
            val = e(value, stack)
            if not isinstance(idx, IntToken):
                raise TypeError("Array index must be an integer")
            if not isinstance(arr, list):
                raise TypeError("Cannot index into non-array")
            if idx.v < 0 or idx.v >= len(arr):
                raise IndexError("Array index out of bounds")
            arr[int(idx.v)] = val
            return val
        # case Fun(name, func_para, func_exp, func_body):   For normal function
        #     stack.append((name, (func_para, func_exp)))
        #     x = e(func_body, stack)
        #     stack.pop()
        #     return x
        # case Call(name, value):
        #     a, b = lookup(stack, name)
        #     stack.append((a, e(value, stack)))
        #     y = e(b, stack)
        #     stack.pop()
        #     return y
        case Fun(parameters, body):
            return (parameters, body, stack.copy())
        case Call(func, args):
            func_value = e(func, stack)
            if not isinstance(func_value, tuple) or len(func_value) != 3:
                raise TypeError("Attempted to call a non-function")
            parameters, body, func_env = func_value
            arg_values = [e(arg, stack) for arg in args]
            if len(parameters) != len(arg_values):
                raise ValueError("Incorrect number of arguments")

            call_env = func_env.copy()
            for param, arg_val in zip(parameters, arg_values):
                param_name = param.v if isinstance(param, Var) else param
                call_env.append((param_name, arg_val))
            return e(body, call_env)
        case Assign(var, expr):
            value = e(expr, stack)
            for i in range(len(stack)-1, -1, -1):
                if stack[i][0] == var:
                    stack[i] = (var, value)
                    return value

            stack.append((var, value))
            return value
        case Let(variable, value_expr, body_expr):
            # if isinstance(value_expr, Fun):
            #     # Create a new environment for the function
            #     func_env = stack.copy()
                
            #     # Create the closure
            #     func_closure = (value_expr.parameters, value_expr.body, func_env)
                
            #     # Add the function to its own environment first
            #     func_env.append((variable.v, func_closure))
                
            #     # Add to current environment
            #     stack.append((variable.v, func_closure))
                
            #     # Evaluate body
            #     result = e(body_expr, stack)
            #     stack.pop()
            #     return result
            if isinstance(value_expr, Fun):
                mutual_env = stack.copy()
                even_closure = (value_expr.parameters, value_expr.body, mutual_env)
                mutual_env.append((variable.v, even_closure))
                stack.append((variable.v, even_closure))
                result = e(body_expr, stack)
                stack.pop()
                return result
            else:
                value = e(value_expr, stack)
                stack.append((variable.v, value))
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
    result = None
    while True:
        condition = e(tree.condition, stack)
        if not (isinstance(condition, BoolToken) and condition.v):
            break
        for expr in tree.body:
            result = e(expr, stack)
    return result