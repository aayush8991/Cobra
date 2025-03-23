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
    body: list[AST]
    _fields = ('condition', 'body')

# @dataclass        normal case
# class Fun(AST):
#     name: str
#     func_para: AST
#     func_exp: AST
#     func_body: AST
#     _fields = ('n', 'a', 'b', 'e')

# @dataclass
# class Call(AST):
#     name: str
#     value: AST
#     _fields = ('n', 'a')

@dataclass
class Fun(AST):
    parameters: list[str] 
    body: AST              
    _fields = ('parameters', 'body')

@dataclass
class Call(AST):
    func: AST 
    args: list[AST] 
    _fields = ('func', 'args')

@dataclass
class Assign(AST):
    var: AST 
    expr: AST  
    _fields = ('var', 'expr')

@dataclass
class Array(AST):
    elements: list[AST]
    _fields = ('elements',)

@dataclass
class ArrayIndex(AST):
    array: AST
    index: AST
    _fields = ('array', 'index')

@dataclass
class ArrayAssign(AST):
    array: AST
    index: AST
    value: AST
    _fields = ('array', 'index', 'value')