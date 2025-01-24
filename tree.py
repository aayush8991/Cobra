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
class VarAssign(AST):
    var_name: str
    value: AST

@dataclass
class VarRef(AST):
    var_name: str

@dataclass
class If(AST):
    c: AST
    t: AST
    e: AST

@dataclass
class WhileLoop(AST):
    condition: AST
    body: list[AST]
