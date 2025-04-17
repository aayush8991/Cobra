enum opcode {
    HALT = 0,    // Stop execution
    // NOP = 1,     // No operation
    PUSH = 1,    // Push value onto stack
    POP = 2,     // Pop value from stack
    ADD = 3,     // Add top two values
    SUB = 4,     // Subtract top two values
    MUL = 5,     // Multiply top two values
    DIV = 6,     // Divide top two values
    NEG = 7,     // Negate top value
    EQ = 8,      // Equal comparison
    LT = 9,      // Less than comparison
    GT = 10,     // Greater than comparison
    JMP = 11,    // Unconditional jump
    JMPF = 12,   // Jump if false
    LOAD = 13,   // Load from environment
    STORE = 14,  // Store in environment
    CALL = 15,   // Function call
    RET = 16,    // Return from function
    ARRAY = 17,  // Create array
    ALOAD = 18,  // Load from array
    ASTORE = 19,  // Store in array
    NOP = 20,     // No operation
};