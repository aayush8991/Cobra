from tree import *
from lexer import *
from more_itertools import peekable
from decimal import Decimal

def parse(s: str) -> AST:
    t = peekable(lex(s))
    def expect(what: Token):
        if t.peek(None) == what:
            next(t)
            return
        raise ParseError
    
    def parse_braced_expr():
        expect(OperatorToken('{'))
        expr = parse_statements()
        expect(OperatorToken('}'))
        return expr

    def parse_statements():
        statements = [parse_print()]
        while t.peek(None) == OperatorToken(';'):
            next(t)
            statements.append(parse_print())
        if len(statements) == 1:
            return statements[0]
        return statements
    
    def parse_print():
        match t.peek(None):
            case KeywordToken("print"):
                next(t)
                expect(OperatorToken('('))
                expr = parse_let()
                expect(OperatorToken(')'))
                return Print(expr)
            case _:
                return parse_let()

    def parse_let():
        match t.peek(None):
            case KeywordToken("let"):
                next(t)
                vt = next(t)
                expect(KeywordToken("be"))
                e = parse_let()
                expect(KeywordToken("in"))
                f = parse_statements()  # Change from parse_let to parse_statements
                expect(KeywordToken("end"))
                return Let(Var(vt.v), e, f)
            case _:
                return parse_fun()

    def parse_fun():
        match t.peek(None):
            case KeywordToken("fun"):
                next(t)
                expect(OperatorToken('('))
                parameters = []
                while t.peek(None) != OperatorToken(')'):
                    parameters.append(Var(next(t).v))
                    if t.peek(None) == OperatorToken(','):
                        next(t)
                expect(OperatorToken(')'))  
                expect(KeywordToken("is"))
                body = parse_statements()
                return Fun(parameters, body)
            case _:
                return parse_if()

    def parse_if():
        match t.peek(None):
            case KeywordToken("if"):
                next(t)
                cond = parse_braced_expr()
                expect(KeywordToken("then"))
                then = parse_statements()
                expect(KeywordToken("else"))
                else_ = parse_statements()
                expect(KeywordToken("end"))
                return If(cond, then, else_)
            case _:
                return parse_while()
            
    def parse_while():
        match t.peek(None):
            case KeywordToken("while"):
                next(t)
                cond = parse_braced_expr()
                expect(KeywordToken("do"))
                body_expr = []
                while t.peek(None) != KeywordToken("end"):
                    body_expr.append(parse_statements())
                expect(KeywordToken("end"))
                return While(cond, body_expr)
            case _:
                return parse_or()

    def parse_or():
        ast = parse_and()
        while True:
            match t.peek(None):
                case KeywordToken("or"):
                    next(t)
                    ast = BinOp("or", ast, parse_and())
                case _:
                    return ast

    def parse_and():
        ast = parse_cmp()
        while True:
            match t.peek(None):
                case KeywordToken("and"):
                    next(t)
                    ast = BinOp("and", ast, parse_cmp())
                case _:
                    return ast

    def parse_cmp():
        l = parse_sub()
        if t.peek(None) == OperatorToken('<'):
            next(t)
            r = parse_sub()
            return BinOp('<', l, r)
        elif t.peek(None) == OperatorToken('<='):
            next(t)
            r = parse_sub()
            return BinOp('<=', l, r)
        elif t.peek(None) == OperatorToken('>'):
            next(t)
            r = parse_sub()
            return BinOp('>', l, r)
        elif t.peek(None) == OperatorToken('>='):
            next(t)
            r = parse_sub()
            return BinOp('>=', l, r)
        elif t.peek(None) == OperatorToken('=='):
            next(t)
            r = parse_sub()
            return BinOp('==', l, r)
        elif t.peek(None) == OperatorToken('!='):
            next(t)
            r = parse_sub()
            return BinOp('!=', l, r)
        else:
            return l

    def parse_sub():
        ast = parse_add()
        while True:
            match t.peek(None):
                case OperatorToken('-'):
                    next(t)
                    ast = BinOp('-', ast, parse_add())
                case _:
                    return ast
                    
    def parse_add():
        ast = parse_mul()
        while True:
            match t.peek(None):
                case OperatorToken('+'):
                    next(t)
                    ast = BinOp('+', ast, parse_mul())
                case _:
                    return ast

    def parse_mul():
        ast = parse_div()
        while True:
            match t.peek(None):
                case OperatorToken('*'):
                    next(t)
                    ast = BinOp("*", ast, parse_div())
                case _:
                    return ast
    
    def parse_div():
        ast = parse_mod()
        match t.peek(None):
            case OperatorToken('//'):
                next(t)
                ast = BinOp("//", ast, parse_mod())
            case OperatorToken('/'):
                next(t)
                ast = BinOp("/", ast, parse_mod())
        return ast
    
    def parse_mod():
        ast = parse_pow()
        match t.peek(None):
            case OperatorToken('%'):
                next(t)
                ast = BinOp("%", ast, parse_pow())
        return ast
    
    def parse_pow():
        ast = parse_atom()
        match t.peek(None):
            case OperatorToken('^'):
                next(t)
                ast = BinOp("^", ast, parse_atom())
        return ast

    def parse_atom():
        match t.peek(None):
            case BoolToken(v):
                next(t)
                return BoolToken(v)
            case IntToken(v):
                next(t)
                return IntToken(v)
            case FloatToken(v):
                next(t)
                return FloatToken(v)
            case StringToken(v):
                next(t)
                return StringToken(v)
            case OperatorToken('('):
                next(t)
                expr = parse_let()  # Parse the expression inside the parentheses
                match t.peek(None):
                    case OperatorToken(')'):
                        next(t)
                        return expr
                    case _:
                        raise ValueError("Missing closing parenthesis")
            case OperatorToken('['):
                next(t)
                if t.peek(None) == OperatorToken('('):
                    # Handle [(value, size)] format
                    next(t)  # consume '('
                    value = parse_let()
                    expect(OperatorToken(','))
                    size = parse_let()
                    expect(OperatorToken(')'))
                    expect(OperatorToken(']'))
                    return ArrayInit(value, size)
                else:
                    # Handle normal array literal
                    elements = []
                    while t.peek(None) != OperatorToken(']'):
                        elements.append(parse_let())
                        if t.peek(None) == OperatorToken(','):
                            next(t)
                    expect(OperatorToken(']'))
                    return Array(elements)
            case OperatorToken('{'):
                next(t)
                entries = {}
                while t.peek(None) != OperatorToken('}'):
                    key = parse_let()
                    if isinstance(key, StringToken):
                        key = key.v  # Convert StringToken to plain string
                    expect(OperatorToken(':'))
                    value = parse_let()
                    entries[key] = value
                    if t.peek(None) == OperatorToken(','):
                        next(t)
                expect(OperatorToken('}'))
                return Map(entries)
            case VariableToken(v):
                var_name = next(t).v
                # if t.peek(None) == OperatorToken('['):
                #     # Array indexing
                #     array_var = Var(var_name)
                #     expect(OperatorToken('['))
                #     index = parse_let()
                #     expect(OperatorToken(']'))
                #     if t.peek(None) == OperatorToken(':='):
                #         # Array assignment
                #         expect(OperatorToken(':='))
                #         value = parse_let()
                #         return ArrayAssign(array_var, index, value)
                #     return ArrayIndex(array_var, index)

                if t.peek(None) == OperatorToken('['):
                    # Array indexing with support for multi-dimensional arrays
                    array_var = Var(var_name)
                    indices = []
                    # Collect all consecutive indices into a list
                    while t.peek(None) == OperatorToken('['):
                        expect(OperatorToken('['))
                        indices.append(parse_let())
                        expect(OperatorToken(']'))
                    # Check if this is an assignment
                    if t.peek(None) == OperatorToken(':='):
                        expect(OperatorToken(':='))
                        value = parse_let()
                        return ArrayAssign(array_var, indices, value)
                    
                    return ArrayIndex(array_var, indices)

                if t.peek(None) == OperatorToken('('):
                    expect(OperatorToken('('))
                    args = []
                    while t.peek(None) != OperatorToken(')'):
                        args.append(parse_let())
                        if t.peek(None) == OperatorToken(','):
                            next(t)
                    expect(OperatorToken(')'))
                    return Call(Var(var_name), args)
                elif t.peek(None) == OperatorToken(':='):
                    expect(OperatorToken(':='))
                    arg = parse_let()
                    return Assign(var_name, arg)
                elif t.peek(None) == OperatorToken('.'):
                    expect(OperatorToken('.'))
                    key = parse_atom()  # Changed from parse_let() to parse_atom()
                    if t.peek(None) == OperatorToken(':='):
                        expect(OperatorToken(':='))
                        value = parse_let()
                        return MapAssign(Var(var_name), key, value)
                    return MapAccess(Var(var_name), key)
                return Var(var_name)
            case KeywordToken("input"):
                next(t)
                expect(OperatorToken('('))
                prompt = parse_let()
                expect(OperatorToken(')'))
                return Input(prompt)
            case KeywordToken("sort"):
                next(t)
                expect(OperatorToken('('))
                array = parse_let()
                expect(OperatorToken(')'))
                return Sort(array)
            case _:
                print(t.peek(None))
                raise ValueError("Unexpected token in expression")

    result = parse_print()
    if result is None:
        raise ValueError("Invalid syntax")
    return result
