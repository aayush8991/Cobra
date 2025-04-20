from tree import *
from lexer import *
from enum import IntEnum

# Instruction Set
class Opcode(IntEnum):
    HALT   = 0    # Stop execution
    PUSH   = 1    # Push value onto stack
    POP    = 2    # Pop value from stack
    ADD    = 3    # Add top two values
    SUB    = 4    # Subtract top two values
    MUL    = 5    # Multiply top two values
    DIV    = 6    # Divide top two values
    NEG    = 7    # Negate top value
    EQ     = 8    # Equal comparison
    LT     = 9    # Less than comparison
    GT     = 10   # Greater than comparison
    JMP    = 11   # Unconditional jump
    JMPF   = 12   # Jump if false
    LOAD   = 13   # Load from environment
    STORE  = 14   # Store in environment
    CALL   = 15   # Function call
    RET    = 16   # Return from function
    ARRAY  = 17   # Create array
    ALOAD  = 18   # Load from array
    ASTORE = 19   # Store in array
    NOP    = 20   # No operation


def do_codegen(t: AST, code, env=None):
    if env is None:
        env = {}

    def emit(opcode, operand=None):
        code.append(opcode)
        if operand is not None:
            code.append(operand)

    match t:
        case IntToken(v):
            emit(Opcode.PUSH, int(v))
        
        case Var(name, _):
            if name not in env:
                raise Exception(f"Undefined variable: {name}")
            emit(Opcode.LOAD, env[name])
        
        case Array(elements):
            emit(Opcode.PUSH, len(elements))
            emit(Opcode.ARRAY)
            for elem in elements:
                do_codegen(elem, code, env)
        
        case ArrayIndex(array, index):
            do_codegen(array, code, env)
            do_codegen(index, code, env)
            emit(Opcode.ALOAD)
        
        case ArrayAssign(array, index, value):
            do_codegen(array, code, env)
            do_codegen(index, code, env)
            do_codegen(value, code, env)
            emit(Opcode.ASTORE)
        
        case BinOp(op, left, right):
            do_codegen(left, code, env)
            do_codegen(right, code, env)
            match op:
                case "+": emit(Opcode.ADD)
                case "-": emit(Opcode.SUB)
                case "*": emit(Opcode.MUL)
                case "/": emit(Opcode.DIV)
                case "==": emit(Opcode.EQ)
                case "<": emit(Opcode.LT)
                case ">": emit(Opcode.GT)
        
        case If(cond, then, else_):
            do_codegen(cond, code, env)
            emit(Opcode.JMPF, 0)
            else_jump = len(code)
            do_codegen(then, code, env.copy())
            emit(Opcode.JMP, 0)
            then_jump = len(code)
            code[else_jump] = len(code)
            do_codegen(else_, code, env.copy())
            code[then_jump] = len(code)
        
        case While(cond, body):
            loop_start = len(code)
            do_codegen(cond, code, env.copy())
            emit(Opcode.JMPF, 0)
            exit_jump = len(code)-1
            for stmt in body:
                do_codegen(stmt, code, env.copy())
            emit(Opcode.JMP, loop_start)
            code[exit_jump] = len(code)
        
        case Fun(parameters, body):
            emit(Opcode.JMP, 0)
            jump_over_func = len(code)-1
            func_start = len(code)
            local_env = env.copy()
            for i, param in enumerate(parameters):
                if isinstance(param, Var):
                    local_env[param.v] = i
            do_codegen(body, code, local_env)
            emit(Opcode.RET)
            code[jump_over_func] = len(code)
            emit(Opcode.PUSH, func_start)

        case Call(func, args):
            for arg in args:
                do_codegen(arg, code, env)
            emit(Opcode.PUSH, len(args))
            do_codegen(func, code, env)
            emit(Opcode.CALL)
        
        case Let(var, val, body):
            do_codegen(val, code, env)
            new_env = env.copy()
            if isinstance(var, Var):
                new_env[var.v] = len(env)
                emit(Opcode.STORE, new_env[var.v])
            do_codegen(body, code, new_env)

        case Assign(var, expr):
            do_codegen(expr, code, env)
            if isinstance(var, Var):
                if var.v not in env:
                    raise Exception(f"Undefined variable: {var.v}")
                emit(Opcode.STORE, env[var.v])

    return code

def codegen(t):
    c = do_codegen(t, bytearray())
    c.append(Opcode.HALT)
    return c

if __name__ == "__main__":
    # Example usage
    expr = Let(
            v=Var(v="add", i=None),
            e=Fun(
                parameters=[Var(v="a", i=None), Var(v="b", i=None)],
                body=BinOp(op="+", left=Var(v="a", i=None), right=Var(v="b", i=None))
            ),
            f=Let(
                v=Var(v="result", i=None),
                e=Call(func=Var(v="add", i=None), args=[IntToken(v=Decimal("1")), IntToken(v=Decimal("2"))]),
                f=Call(func=Var(v="add", i=None), args=[Var(v="result", i=None), IntToken(v=Decimal("3"))])
            )
        )
    bytecode = codegen(expr)
    print(list(bytecode))