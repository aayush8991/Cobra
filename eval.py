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
        case ArrayInit(value, size):
            initial_value = e(value, stack)
            size_value = e(size, stack)
            if not isinstance(size_value, IntToken):
                raise TypeError("Array size must be an integer")
            if size_value.v < 0:
                raise ValueError("Array size cannot be negative")
            # Create a list of the specified size with the initial value
            return [initial_value for _ in range(int(size_value.v))]
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
        case Map(entries):
            evaluated_map = {}
            for key, value in entries.items():
                if isinstance(key, str):  # If key is already a string
                    evaluated_key = key
                else:
                    evaluated_key = e(key, stack)
                    if isinstance(evaluated_key, StringToken):
                        evaluated_key = evaluated_key.v
                evaluated_map[evaluated_key] = e(value, stack)
            return evaluated_map
        case MapAssign(map, key, value):
            map_value = e(map, stack)
            key_value = e(key, stack)
            if isinstance(key_value, StringToken):
                key_value = key_value.v
            value_value = e(value, stack)
            if not isinstance(map_value, dict):
                raise TypeError("Cannot assign to non-map")
            map_value[key_value] = value_value
            return value_value
        case MapAccess(map, key):
            map_value = e(map, stack)
            key_value = e(key, stack)
            if isinstance(key_value, StringToken):
                key_value = key_value.v
            if not isinstance(map_value, dict):
                raise TypeError("Cannot access non-map")
            return map_value[key_value]
        case StringToken(v):
            return StringToken(v)
        case str():  # Handle plain strings
            return StringToken(tree)
        case list():  # Handle list of statements
            result = None
            for stmt in tree:
                result = e(stmt, stack)
            return result
        case Input(prompt):
            prompt_val = e(prompt, stack)
            if isinstance(prompt_val, StringToken):
                user_input = input(prompt_val.v)
                try:
                    # Try to convert to number if possible
                    if '.' in user_input:
                        return FloatToken(Decimal(user_input))
                    return IntToken(Decimal(user_input))
                except:
                    # If not a number, return as string
                    return StringToken(user_input)
            raise TypeError("Input prompt must be a string")
        case Print(value):
            result = e(value, stack)
            if isinstance(result, IntToken):
                print(result.v)
            elif isinstance(result, FloatToken):
                print(result.v)
            elif isinstance(result, StringToken):
                print(result.v)
            elif isinstance(result, list):
                print(result)  
            elif isinstance(result, dict):
                print(result)  
            else:
                print(result)  
            return result
        case _:
            raise ValueError(f"Unknown AST node := {tree}")

def eval_math(tree: BinOp, stack):
    left = e(tree.left, stack)
    right = e(tree.right, stack)

    # Get actual values from tokens
    if isinstance(left, Token):
        left_val = left.v
    else:
        left_val = left

    if isinstance(right, Token):
        right_val = right.v
    else:
        right_val = right

    match tree.op:
        case "or":
            if isinstance(left, (IntToken, BoolToken)) and isinstance(right, (IntToken, BoolToken)):
                left_val = left.v if isinstance(left, IntToken) else int(left.v)
                right_val = right.v if isinstance(right, IntToken) else int(right.v)
                return IntToken(1 if left_val != 0 or right_val != 0 else 0)
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} or {type(right).__name__}")
        case "and":
            if isinstance(left, (IntToken, BoolToken)) and isinstance(right, (IntToken, BoolToken)):
                left_val = left.v if isinstance(left, IntToken) else int(left.v)
                right_val = right.v if isinstance(right, IntToken) else int(right.v)
                return IntToken(1 if left_val != 0 and right_val != 0 else 0)
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} and {type(right).__name__}")
        case "%":
            if isinstance(left, (IntToken, FloatToken)) and isinstance(right, (IntToken, FloatToken)):
                if right.v == 0:
                    raise ZeroDivisionError("Modulo by zero")
                if isinstance(left, FloatToken) or isinstance(right, FloatToken):
                    return FloatToken(left.v % right.v)
                return IntToken(left.v % right.v)
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} % {type(right).__name__}")
        case "+":
            if isinstance(left_val, (int, float, Decimal)) and isinstance(right_val, (int, float, Decimal)):
                result = left_val + right_val
                if isinstance(result, float) or isinstance(left_val, float) or isinstance(right_val, float):
                    return FloatToken(Decimal(str(result)))
                return IntToken(Decimal(str(result)))
            elif isinstance(left_val, str) and isinstance(right_val, str):
                return StringToken(left_val + right_val)
            elif isinstance(left_val, str) and isinstance(right_val, (int, float, Decimal)):
                return StringToken(left_val + str(right_val))
            elif isinstance(left_val, (int, float, Decimal)) and isinstance(right_val, str):
                return StringToken(str(left_val) + right_val)
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
            elif isinstance(left, StringToken) and isinstance(right, StringToken):
                return BoolToken(left.v == right.v)
            elif isinstance(left, BoolToken) and isinstance(right, BoolToken):
                return BoolToken(left.v == right.v)
            else:
                raise TypeError(f"Invalid operation: {type(left).__name__} == {type(right).__name__}")
        case "!=":
            if isinstance(left, (IntToken, FloatToken)) and isinstance(right, (IntToken, FloatToken)):
                return BoolToken(Decimal(left.v) != Decimal(right.v))
            elif isinstance(left, BoolToken) and isinstance(right, BoolToken):
                return BoolToken(left.v != right.v)
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
            # print(result)
    return result