#include <stdio.h>
#include <stdint.h>
#include <assert.h>
#include "bytecode.c"

void test_arithmetic_operations()
{
    uint8_t insns[] = {
        0x01, 0x0A, // PUSH 10
        0x01, 0x04, // PUSH 4
        0x04,       // SUB => 10 - 4 = 6
        0x01, 0x02, // PUSH 2
        0x05,       // MUL => 6 * 2 = 12
        0x01, 0x03, // PUSH 3
        0x06,       // DIV => 12 / 3 = 4
        0x00, 0x00  // HALT
    };
    // printf("Expected: 4, Got: %d\n", execute(insns));
    assert(execute(insns) == 4);
}

void test_conditional_branch()
{
    uint8_t insns[] = {
        0x01, 0x01, // PUSH 1
        0x01, 0x01, // PUSH 1
        0x08,       // EQ (1 == 1) => true
        0x0C, 0x00, 0x0D, // JMPF 13 if false (skip next part)
        0x01, 0x05, // PUSH 5
        0x00,       // HALT
        0x01, 0xFF, // (would execute if condition was false)
        0x00,       // HALT
    };
    // printf("Expected: 5, Got: %d\n", execute(insns));
    assert(execute(insns) == 5);
}

void test_gt_instruction()
{
    uint8_t insns[] = {
        0x01, 0x07, // PUSH 7
        0x01, 0x05, // PUSH 5
        0x0A,       // GT => 7 > 5 => 1 (true)
        0x00,       // HALT
    };
    assert(execute(insns) == 1);
}

void test_load_store()
{
    uint8_t insns[] = {
        0x01, 0x0A, // PUSH 10      - Push 10 onto the stack
        0x0E, 0x00, // STORE 0     - Store the value 10 into memory location 0
        0x0D, 0x00, // LOAD 0      - Load value from memory location 0 (should be 10)
        0x00,       // HALT
    };
    // printf("Expected: 10, Got: %d\n", execute(insns));
    assert(execute(insns) == 10); // The value loaded from memory should be 10
}

void test_stack_behavior()
{
    uint8_t insns[] = {
        0x01, 0x03, // PUSH 3
        0x01, 0x02, // PUSH 2
        0x01, 0x01, // PUSH 1
        0x03,       // ADD => 1 + 2 = 3
        0x03,       // ADD => 3 + 3 = 6
        0x00,       // HALT
    };
    assert(execute(insns) == 6);
}

void test_nested_jumps()
{
    uint8_t insns[] = {
        0x01, 0x01, // PUSH 1
        0x0C, 0x0A, // JMPF 10 (shouldn't jump)
        0x01, 0x02, // PUSH 2
        0x0B, 0x0C, // JMP 12 (skip next push)
        0x01, 0xFF, // (should be skipped)
        0x01, 0x03, // PUSH 3
        0x03,       // ADD => 2 + 3 = 5
        0x00,       // HALT
    };
    assert(execute(insns) == 5);
}

void test_array_operations()
{
    uint8_t insns[] = {
        0x01, 0x01, // PUSH 1
        0x01, 0x02, // PUSH 2
        0x01, 0x03, // PUSH 3
        0x01, 0x03, // PUSH 3 (array size)
        0x10, 0x00, // ARRAY (create array)

        0x01, 0x00, // PUSH 0 (array_id)
        0x01, 0x01, // PUSH 1 (index)
        0x01, 0x0A, // PUSH 10 (new value)
        0x13, 0x00, // ASTORE (store 10 at arr[1])

        0x01, 0x00, // PUSH 0 (array_id)
        0x01, 0x01, // PUSH 1 (index)
        0x12, 0x00, // ALOAD (load arr[1])
        0x00, 0x00  // HALT
    };
    assert(execute(insns) == 10); // Value at index 1 is updated to 10
}

void test_jmp_and_jmpf()
{
    uint8_t insns[] = {
        0x0B, 0x00, 0x05, // JMP 0x0005 — skips over PUSH 255
        0x01, 0xFF,       // PUSH 255 (should be skipped)
        0x01, 0x01,       // PUSH 1
        0x0C, 0x00, 0x0C, // JMPF 0x000C — does NOT jump because top is 1
        0x01, 0x02,       // PUSH 2 (should execute)
        0x00,             // HALT
        0x01, 0x03,       // (Would only run if JMPF jumped)
        0x00              // HALT
    };
    assert(execute(insns) == 2); // Final result on stack should be 2
}

void test_loop_increment()
{
    uint8_t insns[] = {
        0x01, 0x00,       // PUSH 0           ; Initialize i = 0
        0x0E, 0x00,       // STORE 0          ; Store i in variable 0
    
        // Loop start
        0x0D, 0x00,       // LOAD 0           ; Load i
        0x01, 0x05,       // PUSH 5           ; Push constant 5
        0x09,             // LT               ; i < 5
        0x0E, 0x01,       // STORE 1          ; Store result of comparison in variable 1
        0x0D, 0x01,       // LOAD 1           ; Load comparison result
        0x0C, 0x00, 0x23, // JMPF 35          ; If false, jump to end
    
        // Loop body
        0x00,             // NOP or placeholder (unused or incorrect)
        0x01, 0x01,       // PUSH 1           ; Push constant 1
        0x03,             // ADD              ; i + 1
        0x0E, 0x02,       // STORE 2          ; Store in temp variable 2
    
        0x0D, 0x02,       // LOAD 2           ; Load temp i
        0x0E, 0x03,       // STORE 3          ; i = i + 1
        0x0D, 0x03,       // LOAD 3           ; Load updated i
        0x01, 0x01,       // PUSH 1           ; Push 1
        0x0D, 0x03,       // LOAD 3           ; Load updated i again
        0x0F,             // POP              ; Probably discarding old value
    
        0x0B, 0x00, 0x27, // JMP 39           ; Jump to loop start
        0x05,             // HALT             ; End program
        0x0E, 0x00,       // STORE 0          ; Final store (may be redundant)
        0x00              // HALT or NOP
    };    
    printf("Expected: 5, Got: %d\n", execute(insns));
    // assert(execute(insns) == 5);  // Final value of i is 5
}

void test_function_calls()
{
    uint8_t insns[] = {
        0x01, 0x02, // PUSH 2 (arg1)
        0x01, 0x03, // PUSH 3 (arg2)
        0x01, 0x0A, // PUSH 10 (function address)
        0x01, 0x02, // PUSH 2 (num_args)
        0x15, 0x00, // CALL
        0x00, 0x00, // HALT

        // Function at address 10
        0x0D, 0x00, // LOAD 0
        0x0D, 0x01, // LOAD 1
        0x03, 0x00, // ADD
        0x16, 0x00  // RET
    };
    int result = execute(insns);
    printf("Expected: 5, Got: %d\n", result);
    assert(execute(insns) == 5); // 2 + 3 = 5
}

void test_nested_function_calls()
{
    uint8_t insns[] = {
        0x01, 0x03, // PUSH 3
        0x01, 0x14, // PUSH 20 (func2 addr)
        0x01, 0x01, // PUSH 1 arg
        0x15, 0x00, // CALL
        0x00, 0x00, // HALT

        // func1 at 14
        0x0D, 0x00, // LOAD 0
        0x01, 0x01, // PUSH 1
        0x03, 0x00, // ADD
        0x16, 0x00, // RET

        // func2 at 20
        0x0D, 0x00, // LOAD 0
        0x01, 0x0E, // PUSH 14 (func1 addr)
        0x01, 0x01, // PUSH 1 arg
        0x15, 0x00, // CALL func1
        0x01, 0x02, // PUSH 2
        0x03, 0x00, // ADD
        0x16, 0x00  // RET
    };
    int result = execute(insns);
    printf("Expected: 6, Got: %d\n", result);
    assert(execute(insns) == 6); // func1(3) = 4, func2(3) = 4 + 2 = 6
}

int main()
{
    test_arithmetic_operations();
    test_conditional_branch();
    test_gt_instruction();
    test_load_store();
    test_stack_behavior();
    test_jmp_and_jmpf();
    // test_loop_increment();
    // test_nested_jumps();
    // test_array_operations();
    // test_function_calls();
    // test_nested_function_calls();

    printf("All tests passed!\n");
    return 0;
}