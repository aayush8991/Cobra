from tree import *
from lexer import *

# Instruction Set
HALT = 0    # Stop execution
PUSH = 1    # Push value onto stack
POP = 2     # Pop value from stack
ADD = 3     # Add top two values
SUB = 4     # Subtract top two values
MUL = 5     # Multiply top two values
DIV = 6     # Divide top two values
NEG = 7     # Negate top value
EQ = 8      # Equal comparison
LT = 9      # Less than comparison
GT = 10     # Greater than comparison
JMP = 11    # Unconditional jump
JMPF = 12   # Jump if false
LOAD = 13   # Load from environment
STORE = 14  # Store in environment
CALL = 15   # Function call
RET = 16    # Return from function
ARRAY = 17  # Create array
ALOAD = 18  # Load from array
ASTORE = 19 # Store in array

def do_codegen(t: AST, code, env=None):
    if env is None:
        env = {}
        
    def emit(opcode, operand=0):
        code.append(opcode)
        code.append(operand)

    match t:
        case IntToken(v):
            code.append(PUSH)
            code.append(int(v))
            
        case Var(name, _):
            if name not in env:
                env[name] = len(env)
            code.append(LOAD)
            code.append(env[name])
            
        case Array(elements):
            # Push array size
            code.append(PUSH)
            code.append(len(elements))
            code.append(ARRAY)
            # Push elements
            for elem in elements:
                do_codegen(elem, code, env)
                
        case ArrayIndex(array, index):
            do_codegen(array, code, env)
            do_codegen(index, code, env)
            code.append(ALOAD)
            
        case ArrayAssign(array, index, value):
            do_codegen(array, code, env)
            do_codegen(index, code, env)
            do_codegen(value, code, env)
            code.append(ASTORE)
            
        case BinOp(op, left, right):
            do_codegen(left, code, env)
            do_codegen(right, code, env)
            match op:
                case "+": code.append(ADD)
                case "-": code.append(SUB)
                case "*": code.append(MUL)
                case "/": code.append(DIV)
                case "==": code.append(EQ)
                case "<": code.append(LT)
                case ">": code.append(GT)
            
        case If(cond, then, else_):
            do_codegen(cond, code, env)
            code.append(JMPF)
            else_jump = len(code)
            code.append(0)  # placeholder
            do_codegen(then, code, env)
            code.append(JMP)
            then_jump = len(code)
            code.append(0)  # placeholder
            code[else_jump] = len(code)
            do_codegen(else_, code, env)
            code[then_jump] = len(code)
            
        case While(cond, body):
            start = len(code)
            do_codegen(cond, code, env)
            code.append(JMPF)
            cond_jump = len(code)
            code.append(0)  # placeholder
            do_codegen(body, code, env)
            code.append(JMP)
            code.append(start)
            code[cond_jump] = len(code)
            
        case Fun(parameters, body):
            code.append(JMP)
            skip_jump = len(code)
            code.append(0)  # placeholder
            func_start = len(code)
            # Create new environment for function
            func_env = env.copy()
            for param in parameters:
                if isinstance(param, Var):
                    func_env[param.v] = len(func_env)
            do_codegen(body, code, func_env)
            code.append(RET)
            code[skip_jump] = len(code)
            # Push function address
            code.append(PUSH)
            code.append(func_start)
            
        case Call(func, args):
            # Push arguments
            for arg in args:
                do_codegen(arg, code, env)
            # Push number of arguments
            code.append(PUSH)
            code.append(len(args))
            # Generate code for function
            do_codegen(func, code, env)
            code.append(CALL)
            
        case Let(var, val, body):
            do_codegen(val, code, env)
            if isinstance(var, Var):
                if var.v not in env:
                    env[var.v] = len(env)
                code.append(STORE)
                code.append(env[var.v])
            do_codegen(body, code, env)
            
    return code

def codegen(t):
    c = do_codegen(t, bytearray())
    c.append(HALT)
    return c


# expr_cg = BinOp ("*", BinOp("+", IntToken("2"), IntToken("3")), IntToken("5"))
# expr_cg = Let(v=Var(v='arr', i=None), e=Array(elements=[IntToken(v=Decimal('1')), IntToken(v=Decimal('4')), IntToken(v=Decimal('3'))]), f=Let(v=Var(v='sum', i=None), e=Fun(parameters=[Var(v='a', i=None)], body=Let(v=Var(v='i', i=None), e=IntToken(v=Decimal('0')), f=Let(v=Var(v='total', i=None), e=IntToken(v=Decimal('0')), f=While(condition=BinOp(op='<', left=Var(v='i', i=None), right=IntToken(v=Decimal('3'))), body=[Assign(var='i', expr=BinOp(op='+', left=Var(v='i', i=None), right=IntToken(v=Decimal('1')))), Assign(var='total', expr=BinOp(op='+', left=Var(v='total', i=None), right=ArrayIndex(array=Var(v='a', i=None), index=BinOp(op='-', left=Var(v='i', i=None), right=IntToken(v=Decimal('1'))))))])))), f=Call(func=Var(v='sum', i=None), args=[Var(v='arr', i=None)])))
expr_cg = Let(v=Var(v='arr', i=1), e=Array(elements=[IntToken(v=Decimal('1')), IntToken(v=Decimal('4')), IntToken(v=Decimal('3'))]), f=Let(v=Var(v='sum', i=2), e=Fun(parameters=[Var(v='a', i=3)], body=Let(v=Var(v='i', i=4), e=IntToken(v=Decimal('0')), f=Let(v=Var(v='total', i=5), e=IntToken(v=Decimal('0')), f=While(condition=BinOp(op='<', left=Var(v='i', i=4), right=IntToken(v=Decimal('3'))), body=[Assign(var=Var(v='i', i=4), expr=BinOp(op='+', left=Var(v='i', i=4), right=IntToken(v=Decimal('1')))), Assign(var=Var(v='total', i=5), expr=BinOp(op='+', left=Var(v='total', i=5), right=ArrayIndex(array=Var(v='a', i=3), index=BinOp(op='-', left=Var(v='i', i=4), right=IntToken(v=Decimal('1'))))))])))), f=Call(func=Var(v='sum', i=2), args=[Var(v='arr', i=1)])))
print(codegen(expr_cg))

# def codegen(t):
#     c = do_codegen(t, bytearray())
#     c.append(HALT)
    
#     # Write bytecode to file
#     with open("program.bin", "wb") as f:
#         f.write(c)
    
#     return c

# expr_cg = Let(v=Var(v='arr', i=1), e=Array(elements=[IntToken(v=Decimal('1')), IntToken(v=Decimal('4')), IntToken(v=Decimal('3'))]), f=Let(v=Var(v='sum', i=2), e=Fun(parameters=[Var(v='a', i=3)], body=Let(v=Var(v='i', i=4), e=IntToken(v=Decimal('0')), f=Let(v=Var(v='total', i=5), e=IntToken(v=Decimal('0')), f=While(condition=BinOp(op='<', left=Var(v='i', i=4), right=IntToken(v=Decimal('3'))), body=[Assign(var=Var(v='i', i=4), expr=BinOp(op='+', left=Var(v='i', i=4), right=IntToken(v=Decimal('1')))), Assign(var=Var(v='total', i=5), expr=BinOp(op='+', left=Var(v='total', i=5), right=ArrayIndex(array=Var(v='a', i=3), index=BinOp(op='-', left=Var(v='i', i=4), right=IntToken(v=Decimal('1'))))))])))), f=Call(func=Var(v='sum', i=2), args=[Var(v='arr', i=1)])))
# print(codegen(expr_cg))