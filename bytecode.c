#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include "opcode.h"

#define STACK_SIZE 1000
#define ENV_SIZE 1000
#define HEAP_SIZE 1000

typedef struct {
    int *data;
    int size;
} Array;

int execute(uint8_t *insns) {
    size_t ip = 0;
    int operand[STACK_SIZE], top = 0;
    int env[ENV_SIZE] = {0};
    int env_size = 0;
    Array *heap[HEAP_SIZE] = {NULL};
    int heap_size = 0;

#define PUSH(x) (operand[top++] = (x))
#define POP() (operand[--top])

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
                top--;
                break;
            case ADD:
                r = POP(); l = POP(); PUSH(l+r); 
                break;
            case SUB:
                r = POP(); l = POP(); PUSH(l-r); 
                break;
            case MUL:
                r = POP(); l = POP(); PUSH(l*r); 
                break;
            case DIV:
                r = POP(); l = POP(); PUSH(l/r); 
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
                PUSH(env[insns[ip+1]]); 
                break;
            case STORE:
                env[insns[ip+1]] = POP(); 
                break;
            case ARRAY: {
                int size = POP();
                Array *arr = malloc(sizeof(Array));
                arr->data = malloc(size * sizeof(int));
                arr->size = size;
                for (int i = size-1; i >= 0; i--) {
                    arr->data[i] = POP();
                }
                heap[heap_size] = arr;
                PUSH(heap_size++);
                break;
            }
            case ALOAD: {
                int index = POP();
                int array_id = POP();
                Array *arr = heap[array_id];
                if (index < 0 || index >= arr->size) {
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
                Array *arr = heap[array_id];
                if (index < 0 || index >= arr->size) {
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
                // Save current environment and IP
                PUSH(ip + 2);
                PUSH(env_size);
                // Set up new environment with arguments
                for (int i = 0; i < num_args; i++) {
                    env[env_size++] = POP();
                }
                ip = func_addr;
                continue;
            }
            case RET: {
                int return_value = POP();
                env_size = POP();
                ip = POP();
                PUSH(return_value);
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
}

// Test program
int main() {
    // Example: Create array [1,2,3], set arr[1] = 10, return arr[1]
    uint8_t insns[] = {
        PUSH, 1,
        PUSH, 2,
        PUSH, 3,
        PUSH, 3,  // array size
        ARRAY, 0,
        PUSH, 0,  // array_id
        PUSH, 1,  // index
        PUSH, 10, // new value
        ASTORE, 0,
        PUSH, 0,  // array_id
        PUSH, 1,  // index
        ALOAD, 0,
        HALT, 0
    };
    
    printf("Result: %d\n", execute(insns));
    return 0;
}

// int main() {
//     FILE *fp;
//     long file_size;
//     uint8_t *buffer;

//     // Open the binary file
//     printf("Hi\n");
//     fp = fopen("program.bin", "rb");
//     if (!fp) {
//         fprintf(stderr, "Could not open program.bin\n");
//         return 1;
//     }

//     // Get file size
//     fseek(fp, 0, SEEK_END);
//     file_size = ftell(fp);
//     rewind(fp);

//     // Allocate memory for the bytecode
//     buffer = (uint8_t*)malloc(file_size);
//     if (!buffer) {
//         fprintf(stderr, "Memory allocation failed\n");
//         fclose(fp);
//         return 1;
//     }

//     // Read the bytecode
//     if (fread(buffer, 1, file_size, fp) != file_size) {
//         fprintf(stderr, "Failed to read program.bin\n");
//         free(buffer);
//         fclose(fp);
//         return 1;
//     }

//     fclose(fp);

//     // Execute the bytecode
//     int result = execute(buffer);
//     printf("Result: %d\n", result);

//     free(buffer);
//     return 0;
// }