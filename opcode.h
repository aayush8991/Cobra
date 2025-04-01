enum opcode {
    HALT = 0,    // Stop execution
    NOP = 1,     // No operation
    PUSH = 2,    // Push value onto stack
    POP = 3,     // Pop value from stack
    ADD = 4,     // Add top two values
    SUB = 5,     // Subtract top two values
    MUL = 6,     // Multiply top two values
    DIV = 7,     // Divide top two values
    NEG = 8,     // Negate top value
    EQ = 9,      // Equal comparison
    LT = 10,     // Less than comparison
    GT = 11,     // Greater than comparison
    JMP = 12,    // Unconditional jump
    JMPF = 13,   // Jump if false
    LOAD = 14,   // Load from environment
    STORE = 15,  // Store in environment
    CALL = 16,   // Function call
    RET = 17,    // Return from function
    ARRAY = 18,  // Create array
    ALOAD = 19,  // Load from array
    ASTORE = 20  // Store in array
};