#ifndef BYTECODE_DEFS_H
#define BYTECODE_DEFS_H

// Bytecode opcodes
#define HALT    0
#define PUSH    1
#define POP     2
#define ADD     3
#define SUB     4
#define MUL     5
#define DIV     6
#define NEG     7
#define EQ      8
#define LT      9
#define GT      10
#define JMP     11
#define JMPF    12
#define LOAD    13
#define STORE   14
#define CALL    15
#define RET     16
#define ARRAY   17
#define ALOAD   18
#define ASTORE  19
#define NOP     20
#define MOD     21
#define LE      22
#define GE       23
#define DUP     24  // Duplicate a value on the stack
#define SWAPDUP 25  // Swap with value at offset, then duplicate
#define JMPT    26  // Jump if true

#endif // BYTECODE_DEFS_H