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

@dataclass
class Var(AST):
    v: str

@dataclass
class If(AST):
    cond: AST
    then: AST
    else_: AST

@dataclass
class WhileLoop(AST):
    condition: AST
    body: list[AST]
