import sys
import os
from lexer import *
from parser import parse
from resolver import resolve
from tree import *

# Instruction Set
HALT = 0
PUSH = 1
POP = 2
ADD = 3
SUB = 4
MUL = 5
DIV = 6
NEG = 7
EQ = 8
LT = 9
GT = 10
JMP = 11
JMPF = 12
LOAD = 13
STORE = 14
CALL = 15
RET = 16
ARRAY = 17
ALOAD = 18
ASTORE = 19
NOP = 20
MOD = 21
LE = 22
GE = 23
DUP = 24
SWAPDUP = 25
JMPT = 26

def codegen(t: AST):
    code = []
    env = {}
    
    def emit(opcode, operand=0):
        code.append(opcode)
        code.append(operand)
    
    def do_codegen(t):
        nonlocal env
        
        if isinstance(t, IntToken):
            emit(PUSH, int(t.v))
        
        elif isinstance(t, BinOp):
            do_codegen(t.left)
            do_codegen(t.right)
            match t.op:
                case "+": emit(ADD)
                case "-": emit(SUB)
                case "*": emit(MUL)
                case "/": emit(DIV)
                case "%": emit(MOD)
                case "==": emit(EQ)
                case "<": emit(LT)
                case ">": emit(GT)
                case "<=": emit(LE)
                case ">=": emit(GE)
                case _: raise ValueError(f"Unknown operation: {t.op}")
        
        elif isinstance(t, Var):
            if t.v not in env:
                env[t.v] = len(env)
            emit(LOAD, env[t.v])
        
        elif isinstance(t, Assign):
            var_name = t.var.v if isinstance(t.var, Var) else t.var
            do_codegen(t.expr)
            if var_name not in env:
                env[var_name] = len(env)
            emit(STORE, env[var_name])
        
        elif isinstance(t, While):
            start = len(code)
            do_codegen(t.condition)
            emit(JMPF, 0)  # placeholder
            cond_jump = len(code) - 1
            for stmt in t.body:
                do_codegen(stmt)
            emit(JMP, start)
            code[cond_jump] = len(code)
        
        elif isinstance(t, Let):
            if isinstance(t.v, Var):
                if t.v.v not in env:
                    env[t.v.v] = len(env)
                do_codegen(t.e)
                emit(STORE, env[t.v.v])
            else:
                do_codegen(t.e)
            do_codegen(t.f)
        
        elif isinstance(t, ArrayInit):
            do_codegen(t.size)
            emit(ARRAY)
            do_codegen(t.value)
            emit(PUSH, 0)  # Start index
            loop_start = len(code)
            emit(DUP, 1)  # Duplicate the value
            emit(SWAPDUP, 3)  # Swap and duplicate the index and array
            emit(ASTORE)  # Store the value at current index
            emit(PUSH, 1)
            emit(ADD)  # Increment index
            emit(SWAPDUP, 1)  # Get array size for comparison
            emit(LT)  # Check if index < size
            emit(JMPT, loop_start)
            emit(POP)  # Remove the index
        
        elif isinstance(t, Array):
            emit(PUSH, len(t.elements))
            emit(ARRAY)
            # Now the array ID is on the stack
            
            # For each element
            for i, elem in enumerate(t.elements):
                if i > 0:
                    emit(DUP, 0)  # Duplicate the array ID for each store after the first
                emit(PUSH, i)     # Index
                do_codegen(elem)  # Generate value
                emit(ASTORE)      # Store: consumes array_id, index, value and pushes array_id back
            
            # After the loop, array ID is still on the stack
        
        elif isinstance(t, ArrayIndex):
            do_codegen(t.array)
            if isinstance(t.index, list):
                # Multi-dimensional array
                for idx in t.index:
                    do_codegen(idx)
                    emit(ALOAD)
                    # The loaded value might be another array for multi-dim
            else:
                do_codegen(t.index)
                emit(ALOAD)
        
        elif isinstance(t, ArrayAssign):
            do_codegen(t.array)
            if isinstance(t.index, list):
                # Handle multi-dimensional arrays
                for idx in t.index[:-1]:  # All but last index for navigation
                    do_codegen(idx)
                    emit(ALOAD)
                do_codegen(t.index[-1])  # Last index for assignment
            else:
                do_codegen(t.index)
            do_codegen(t.value)
            emit(ASTORE)
        
        elif isinstance(t, list):
            for stmt in t:
                do_codegen(stmt)
        
        elif isinstance(t, If):
            do_codegen(t.cond)
            emit(JMPF, 0)  # placeholder
            cond_jump = len(code) - 1
            do_codegen(t.then)
            emit(JMP, 0)  # placeholder
            then_jump = len(code) - 1
            code[cond_jump] = len(code)
            do_codegen(t.else_)
            code[then_jump] = len(code)
        
        else:
            print(f"Skipping node type: {type(t).__name__}")  # Debug info
    
    do_codegen(t)
    emit(HALT)
    return bytes(code)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)
    
    with open(sys.argv[1], "r") as f:
        code = f.read()
    
    ast = parse(code)
    abt = resolve(ast)
    bytecode = codegen(abt)
    
    with open(sys.argv[2], "wb") as f:
        f.write(bytecode)
    
    print(f"Generated bytecode to {sys.argv[2]}")