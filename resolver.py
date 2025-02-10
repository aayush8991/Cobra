"""
Converts the AST into an ABT
Uses de Bruijn indices to resolve variable bindings
"""

from tree import *
from lexer import IntToken

def lookup(env, v):
    """Lookup the de Bruijn index of a variable."""
    for i, (u, _) in enumerate(reversed(env)):
        if u == v:
            return i  # Distance from binding
    raise ValueError(f"Unbound variable: {v}")

def resolve(t: AST, env=None) -> AST:
    if env is None:
        env = []
        
    match t:
        case IntToken(n):
            return IntToken(n)

        case Var(x, _):
            return Var(x, lookup(env, x))

        case Let(Var(x, _), e, f):
            er = resolve(e, env)
            env.append((x, None))
            fr = resolve(f, env)
            env.pop()
            return Let(Var(x, 0), er, fr)

        case Fun(f, Var(x, _), b, y):
            env.append((x, None))
            br = resolve(b, env)
            yr = resolve(y, env)
            env.pop()
            return Fun(f, Var(x, 0), br, yr)

        case Call(f, x):
            return Call(resolve(f, env), resolve(x, env))

        case BinOp(op, left, right):
            return BinOp(op, resolve(left, env), resolve(right, env))

        case If(cond, then, else_):
            return If(resolve(cond, env), resolve(then, env), resolve(else_, env))

        case While(condition, body):
            return While(resolve(condition, env), resolve(body, env))

        case _:
            return t
