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
    v: str
    e: AST
    f: AST
    _fields = ('v', 'e', 'f')

@dataclass
class Var(AST):
    v: str

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
