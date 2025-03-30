from tree import *
from lexer import *

def lookup(env, v):
    for u, uv in reversed(env):
        if u == v:
            return uv
    raise ValueError("No value found.")

def make_fresh():
    i = 0
    def fresh():
        nonlocal i
        i = i + 1
        return i
    return fresh

def resolve(t: AST, env = None, fresh = None) -> AST:
    if env is None:
        env = []
    if fresh is None: 
        fresh = make_fresh()
        
    match t:
        case IntToken(n):
            return IntToken(n)
        case Var(x, _):
            return Var(x, lookup(env, x))
        case Let(Var(x, _), e, f):
            # er = resolve(e, env, fresh) normal case
            # env.append((x, i := fresh()))
            # fr = resolve(f, env, fresh)
            # env.pop()
            # return Let(Var(x, i), er, fr)
            if isinstance(e, Fun):
                env.append((x, i := fresh()))
                er = resolve(e, env, fresh)
                fr = resolve(f, env, fresh)
                env.pop()
                return Let(Var(x, i), er, fr)
            else:
                er = resolve(e, env, fresh)
                env.append((x, i := fresh()))
                fr = resolve(f, env, fresh)
                env.pop()
                return Let(Var(x, i), er, fr)
        case Assign(var, expr):
            expr_resolved = resolve(expr, env, fresh)
            try:
                var_id = lookup(env, var)
                return Assign(Var(var, var_id), expr_resolved)
            except ValueError:
                env.append((var, i := fresh()))
                result = Assign(Var(var, i), expr_resolved)
                return result
        # case Fun(f, Var(x, _), b, y):     normal case
        #     env.append((x, i := fresh()))
        #     br = resolve(b, env, fresh)
        #     env.pop()
        #     yr = resolve(y, env, fresh)
        #     return Fun(f, Var(x, i), br, yr)
        # case Call(f, x):
        #     xr = resolve(x, env, fresh)
        #     return Call(f, xr)
        case Fun(parameters, body):
            param_names = [param.v for param in parameters]
            param_ids = [fresh() for _ in param_names]
            env.extend(zip(param_names, param_ids))
            body_resolved = resolve(body, env, fresh)
            for _ in param_names:
                env.pop()
            
            return Fun([Var(name, param_id) for name, param_id in zip(param_names, param_ids)], body_resolved)
        case Call(func, args):
            func_resolved = resolve(func, env, fresh)
            args_resolved = [resolve(arg, env, fresh) for arg in args]
            return Call(func_resolved, args_resolved)
        case Array(elements):
            return Array([resolve(elem, env, fresh) for elem in elements])
        case ArrayIndex(array, index):
            return ArrayIndex(
                resolve(array, env, fresh),
                resolve(index, env, fresh)
            )
        case ArrayAssign(array, index, value):
            return ArrayAssign(
                resolve(array, env, fresh),
                resolve(index, env, fresh),
                resolve(value, env, fresh)
            )
        case BinOp(op, left, right):
            return BinOp(op, resolve(left, env, fresh), resolve(right, env, fresh))
        case If(cond, then, else_):
            return If(resolve(cond, env, fresh), resolve(then, env, fresh), resolve(else_, env, fresh))
        case While(condition, body):
            condition_resolved = resolve(condition, env, fresh)            
            body_resolved = []
            for expr in body:
                body_resolved.append(resolve(expr, env, fresh))
            return While(condition_resolved, body_resolved)
        case Map(entries):
            resolved_entries = {resolve(key, env, fresh): resolve(value, env, fresh) for key, value in entries.items()}
            return Map(resolved_entries)
        case MapAssign(map, key, value):
            return MapAssign(resolve(map, env, fresh), resolve(key, env, fresh), resolve(value, env, fresh))
        case MapAccess(map, key):
            return MapAccess(resolve(map, env, fresh), resolve(key, env, fresh))
        case ArrayInit(value, size):
            return ArrayInit(
                resolve(value, env, fresh),
                resolve(size, env, fresh)
            )
        case Print(value):
            return Print(resolve(value, env, fresh))
        case _:
            return t
        
