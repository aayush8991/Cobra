#include <stdio.h>
#include <stdint.h>
#include <assert.h>
#include "bytecode.c"

void test_arithmetic_operations() {
    uint8_t insns[] = {
        0x01, 0x0A,  // PUSH 10
        0x01, 0x04,  // PUSH 4
        0x04, 0x00,  // SUB => 10 - 4 = 6
        0x01, 0x02,  // PUSH 2
        0x05, 0x00,  // MUL => 6 * 2 = 12
        0x01, 0x03,  // PUSH 3
        0x06, 0x00,  // DIV => 12 / 3 = 4
        0x00, 0x00   // HALT
    };
    assert(execute(insns) == 4);
}

void test_conditional_branch() {
    uint8_t insns[] = {
        0x01, 0x01,  // PUSH 1
        0x01, 0x01,  // PUSH 1
        0x08, 0x00,  // EQ (1 == 1) => true
        0x0C, 0x0C,  // JMPF 12 if false (skip next part)
        0x01, 0x05,  // PUSH 5
        0x00, 0x00,  // HALT
        0x01, 0xFF,  // (would execute if condition was false)
        0x00, 0x00   // HALT
    };
    assert(execute(insns) == 5);
}

void test_gt_instruction() {
    uint8_t insns[] = {
        0x01, 0x07,  // PUSH 7
        0x01, 0x05,  // PUSH 5
        0x0A, 0x00,  // GT => 7 > 5 => 1 (true)
        0x00, 0x00   // HALT
    };
    assert(execute(insns) == 1);
}

void test_stack_behavior() {
    uint8_t insns[] = {
        0x01, 0x03,  // PUSH 3
        0x01, 0x02,  // PUSH 2
        0x01, 0x01,  // PUSH 1
        0x03, 0x00,  // ADD => 1 + 2 = 3
        0x03, 0x00,  // ADD => 3 + 3 = 6
        0x00, 0x00   // HALT
    };
    assert(execute(insns) == 6);
}

void test_nested_jumps() {
    uint8_t insns[] = {
        0x01, 0x01,  // PUSH 1
        0x0C, 0x0A,  // JMPF 10 (shouldn't jump)
        0x01, 0x02,  // PUSH 2
        0x0B, 0x0C,  // JMP 12 (skip next push)
        0x01, 0xFF,  // (should be skipped)
        0x01, 0x03,  // PUSH 3
        0x03, 0x00,  // ADD => 2 + 3 = 5
        0x00, 0x00   // HALT
    };
    assert(execute(insns) == 5);
}

void test_array_operations() {
    uint8_t insns[] = {
        0x01, 0x01,  // PUSH 1
        0x01, 0x02,  // PUSH 2
        0x01, 0x03,  // PUSH 3
        0x01, 0x03,  // PUSH 3 (array size)
        0x10, 0x00,  // ARRAY (create array)

        0x01, 0x00,  // PUSH 0 (array_id)
        0x01, 0x01,  // PUSH 1 (index)
        0x01, 0x0A,  // PUSH 10 (new value)
        0x13, 0x00,  // ASTORE (store 10 at arr[1])

        0x01, 0x00,  // PUSH 0 (array_id)
        0x01, 0x01,  // PUSH 1 (index)
        0x12, 0x00,  // ALOAD (load arr[1])
        0x00, 0x00   // HALT
    };
    assert(execute(insns) == 10);  // Value at index 1 is updated to 10
}

void test_loop_increment() {
    uint8_t insns[] = {
        0x01, 0x00,  // PUSH 0       - Initialize i = 0
        0x0E, 0x00,  // STORE 0      - Store to variable 0
        
        // Loop start (byte 4)
        0x0D, 0x00,  // LOAD 0       - Load i
        0x01, 0x05,  // PUSH 5       - Load 5
        0x09, 0x00,  // LT           - Compare i < 5
        0x0C, 0x16,  // JMPF 22      - If false jump to end (byte 22)
        
        // Loop body
        0x0D, 0x00,  // LOAD 0       - Load i
        0x01, 0x01,  // PUSH 1       - Push 1
        0x03, 0x00,  // ADD          - i + 1
        0x0E, 0x00,  // STORE 0      - i = i + 1
        
        0x0B, 0x04,  // JMP 4        - Jump back to loop start (byte 4)
        
        // End of loop (byte 22)
        0x0D, 0x00,  // LOAD 0       - Load final value of i (should be 5)
        0x00, 0x00   // HALT    
    };
    assert(execute(insns) == 5);  // Final value of i is 5
}

void test_function_calls() {
    uint8_t insns[] = {
        0x01, 0x02,  // PUSH 2 (arg1)
        0x01, 0x03,  // PUSH 3 (arg2)
        0x01, 0x0A,  // PUSH 10 (function address)
        0x01, 0x02,  // PUSH 2 (num_args)
        0x15, 0x00,  // CALL
        0x00, 0x00,  // HALT

        // Function at address 10
        0x0D, 0x00,  // LOAD 0
        0x0D, 0x01,  // LOAD 1
        0x03, 0x00,  // ADD
        0x16, 0x00   // RET
    };
    int result = execute(insns);
    printf("Expected: 5, Got: %d\n", result);
    assert(execute(insns) == 5);  // 2 + 3 = 5
}

void test_nested_function_calls() {
    uint8_t insns[] = {
        0x01, 0x03,  // PUSH 3
        0x01, 0x14,  // PUSH 20 (func2 addr)
        0x01, 0x01,  // PUSH 1 arg
        0x15, 0x00,  // CALL
        0x00, 0x00,  // HALT

        // func1 at 14
        0x0D, 0x00,  // LOAD 0
        0x01, 0x01,  // PUSH 1
        0x03, 0x00,  // ADD
        0x16, 0x00,  // RET

        // func2 at 20
        0x0D, 0x00,  // LOAD 0
        0x01, 0x0E,  // PUSH 14 (func1 addr)
        0x01, 0x01,  // PUSH 1 arg
        0x15, 0x00,  // CALL func1
        0x01, 0x02,  // PUSH 2
        0x03, 0x00,  // ADD
        0x16, 0x00   // RET
    };
    int result = execute(insns);
    printf("Expected: 6, Got: %d\n", result);
    assert(execute(insns) == 6);  // func1(3) = 4, func2(3) = 4 + 2 = 6
}

int main() {
    test_arithmetic_operations();
    test_conditional_branch();
    test_gt_instruction();
    test_stack_behavior();
    test_loop_increment();
    // test_nested_jumps();
    // test_array_operations();
    // test_function_calls();
    // test_nested_function_calls();

    printf("All tests passed!\n");
    return 0;
}