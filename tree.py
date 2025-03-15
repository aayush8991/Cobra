from dataclasses import dataclass

# Abstract Syntax Tree classes
class AST:
    pass

@dataclass
class BinOp(AST):
    op: str
    left: AST
    right: AST
    _fields = ('op', 'left', 'right')

@dataclass
class Let(AST):
    v: AST
    e: AST
    f: AST
    _fields = ('v', 'e', 'f')

@dataclass
class Var(AST):
    v: str
    i: int = None

@dataclass
class If(AST):
    cond: AST
    then: AST
    else_: AST
    _fields = ('cond', 'then', 'else_')

@dataclass
class While(AST):
    condition: AST
    body: AST
    _fields = ('condition', 'body')

@dataclass
class Fun(AST):
    name: str
    func_para: AST
    func_exp: AST
    func_body: AST
    _fields = ('n', 'a', 'b', 'e')

@dataclass
class Call(AST):
    name: str
    value: AST
    _fields = ('n', 'a')