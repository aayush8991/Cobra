#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "opcode.h"

#define STACK_SIZE 1000
#define ENV_SIZE 1000
#define HEAP_SIZE 1000
#define FUN_STACK_SIZE 1000

typedef struct {
    int *data;
    int size;
} Array;

typedef struct {
    size_t ip;
    int env_size;
} FunStack;

int execute(uint8_t *insns) {
    size_t ip = 0;
    int operand[STACK_SIZE], top = 0;
    int env[ENV_SIZE] = {0};
    int env_size = 0;
    Array *heap[HEAP_SIZE] = {NULL};
    int heap_size = 0;

    FunStack fun_stack[FUN_STACK_SIZE];
    int fun_top = 0;

#define PUSH(x) do { \
    if (top >= STACK_SIZE) { \
        fprintf(stderr, "Stack overflow!\n"); \
        exit(1); \
    } \
    operand[top++] = (x); \
} while(0)

#define POP() (top <= 0 ? (fprintf(stderr, "Stack underflow!\n"), exit(1), 0) : operand[--top])

#define FUN_PUSH(ip_val, env_size_val) do { \
    if (fun_top >= FUN_STACK_SIZE) { \
        fprintf(stderr, "Function stack overflow!\n"); \
        exit(1); \
    } \
    fun_stack[fun_top].ip = ip_val; \
    fun_stack[fun_top].env_size = env_size_val; \
    fun_top++; \
} while(0)

#define FUN_POP() (fun_top <= 0 ? (fprintf(stderr, "Function stack underflow!\n"), exit(1), (FunStack){0}) : fun_stack[--fun_top])

    int l, r;
    while (1) {
        switch (insns[ip]) {
            case HALT: 
                goto end;
            case NOP: 
                break;
            case PUSH:
                PUSH(insns[ip+1]); 
                break;
            case POP:
                if (top <= 0) {  // Prevent underflow
                    fprintf(stderr, "Stack underflow!\n");
                    exit(1);
                }
                top--;
                break;
            case ADD:
                r = POP(); l = POP(); PUSH(l + r); 
                break;
            case SUB:
                r = POP(); l = POP(); PUSH(l - r); 
                break;
            case MUL:
                r = POP(); l = POP(); PUSH(l * r); 
                break;
            case DIV:
                r = POP(); 
                if (r == 0) {  // Prevent division by zero
                    fprintf(stderr, "Division by zero!\n");
                    exit(1);
                }
                l = POP(); 
                PUSH(l / r); 
                break;
            case NEG:
                l = POP(); PUSH(-l); 
                break;
            case EQ:
                r = POP(); l = POP(); PUSH(l == r); 
                break;
            case LT:
                r = POP(); l = POP(); PUSH(l < r); 
                break;
            case GT:
                r = POP(); l = POP(); PUSH(l > r); 
                break;
            case JMP:
                ip = insns[ip+1];
                continue;
            case JMPF:
                if (!POP()) {
                    ip = insns[ip+1];
                    continue;
                }
                break;
            case LOAD:
                if (insns[ip+1] >= ENV_SIZE) {  // Prevent out-of-bounds access
                    fprintf(stderr, "Environment index out of bounds\n");
                    exit(1);
                }
                PUSH(env[insns[ip+1]]); 
                break;
            case STORE:
                if (insns[ip+1] >= ENV_SIZE) {  // Prevent out-of-bounds access
                    fprintf(stderr, "Environment index out of bounds\n");
                    exit(1);
                }
                env[insns[ip+1]] = POP(); 
                break;
            case ARRAY: {
                int size = POP();
                if (size <= 0 || heap_size >= HEAP_SIZE) {  // Prevent invalid array size or heap overflow
                    fprintf(stderr, "Invalid array size or heap overflow\n");
                    exit(1);
                }
                Array *arr = malloc(sizeof(Array));
                if (!arr) {
                    fprintf(stderr, "Heap allocation failed\n");
                    exit(1);
                }
                arr->data = malloc(size * sizeof(int));
                if (!arr->data) {
                    fprintf(stderr, "Heap allocation failed\n");
                    free(arr);
                    exit(1);
                }
                arr->size = size;
                for (int i = size - 1; i >= 0; i--) {
                    arr->data[i] = POP();
                }
                heap[heap_size] = arr;
                PUSH(heap_size++);
                break;
            }
            case ALOAD: {
                int index = POP();
                int array_id = POP();
                if (array_id < 0 || array_id >= heap_size || !heap[array_id]) {  // Prevent invalid array access
                    fprintf(stderr, "Invalid array ID\n");
                    exit(1);
                }
                Array *arr = heap[array_id];
                if (index < 0 || index >= arr->size) {  // Prevent out-of-bounds access
                    fprintf(stderr, "Array index out of bounds\n");
                    exit(1);
                }
                PUSH(arr->data[index]);
                break;
            }
            case ASTORE: {
                int value = POP();
                int index = POP();
                int array_id = POP();
                if (array_id < 0 || array_id >= heap_size || !heap[array_id]) {  // Prevent invalid array access
                    fprintf(stderr, "Invalid array ID\n");
                    exit(1);
                }
                Array *arr = heap[array_id];
                if (index < 0 || index >= arr->size) {  // Prevent out-of-bounds access
                    fprintf(stderr, "Array index out of bounds\n");
                    exit(1);
                }
                arr->data[index] = value;
                PUSH(value);
                break;
            }
            case CALL: {
                int func_addr = POP();
                int num_args = POP();
                if (func_addr < 0 || num_args < 0 || env_size + num_args >= ENV_SIZE) {  // Prevent invalid function call
                    fprintf(stderr, "Invalid function call\n");
                    exit(1);
                }
                // Save current environment and IP to function stack
                FUN_PUSH(ip + 2, env_size);
                // Set up new environment with arguments
                for (int i = 0; i < num_args; i++) {
                    env[env_size++] = POP();
                }
                ip = func_addr;  // Jump to the function address
                continue;
            }
            case RET: {
                if (top < 2) {  // Prevent underflow during return
                    fprintf(stderr, "Stack underflow during return\n");
                    exit(1);
                }
                int return_value = POP();  // Pop return value
                FunStack state = FUN_POP();  // Restore state from function stack
                env_size = state.env_size;
                ip = state.ip;
                PUSH(return_value);  // Push return value to the operand stack
                continue;
            }
        }
        ip += 2;
    }
end:
    // Clean up heap
    for (int i = 0; i < heap_size; i++) {
        if (heap[i]) {
            free(heap[i]->data);
            free(heap[i]);
        }
    }
    return POP();
#undef PUSH
#undef POP
#undef FUN_PUSH
#undef FUN_POP
}
