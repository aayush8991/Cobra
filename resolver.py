from tree import *
from lexer import Token
def make_fresh():
    i = 0
    def fresh():
        nonlocal i
        i = i + 1
        return i
    return fresh

env = []

def lookup(v):
    """
    Lookup a variable in the global environment.
    """
    for u, uv in reversed(env):
        if u == v:
            return uv
    raise ValueError("No value found.")

def resolve(t: AST, env = None, fresh = None) -> AST:
    if env is None: env = []
    if fresh is None: fresh = make_fresh()

    match t:
        case Token(n):
            return Token(n)
        case Let(Var(x, _), e, f):
            er = resolve(e, env, fresh)
            env.append((x, i := fresh()))
            fr = resolve(f, env, fresh)
            env.pop()
            return Let(Var(x, i), er, fr)
        case Var(x, _):
            return Var(x, lookup(env, x))
        case Call(f, x):
            xr = resolve(x, env, fresh)
            return Call(f, xr)
        case Fun(f, Var(x, _), b, y):
            env.append((x, i := fresh()))
            br = resolve(b, env, fresh)
            env.pop()
            yr = resolve(y, env, fresh)
            return Fun(f, Var(x, i), br, yr)