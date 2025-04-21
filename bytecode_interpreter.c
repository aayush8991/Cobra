#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "bytecode_defs.h"

#define STACK_SIZE 1024
#define MEMORY_SIZE 1024
#define MAX_ARRAYS 256

typedef struct {
    int* data;
    int size;
} Array;

typedef struct {
    int stack[STACK_SIZE];
    int sp;
    int memory[MEMORY_SIZE];
    int pc;
    Array arrays[MAX_ARRAYS];
    int array_count;
} VM;

void vm_init(VM* vm) {
    vm->sp = 0;
    vm->pc = 0;
    vm->array_count = 0;
    memset(vm->memory, 0, sizeof(vm->memory));
    memset(vm->arrays, 0, sizeof(vm->arrays));
}

void push(VM* vm, int value) {
    if (vm->sp >= STACK_SIZE) {
        fprintf(stderr, "Stack overflow\n");
        exit(1);
    }
    vm->stack[vm->sp++] = value;
}

int pop(VM* vm) {
    if (vm->sp <= 0) {
        fprintf(stderr, "Stack underflow\n");
        exit(1);
    }
    return vm->stack[--vm->sp];
}

void execute(VM* vm, unsigned char* bytecode, int size) {
    while (vm->pc < size) {
        unsigned char opcode = bytecode[vm->pc++];
        unsigned char operand = bytecode[vm->pc++];
        
        switch (opcode) {
            case HALT:
                return;
                
            case PUSH:
                push(vm, operand);
                break;
                
            case POP:
                pop(vm);
                break;
                
            case ADD: {
                int b = pop(vm);
                int a = pop(vm);
                push(vm, a + b);
                break;
            }
            
            case SUB: {
                int b = pop(vm);
                int a = pop(vm);
                push(vm, a - b);
                break;
            }
            
            case MUL: {
                int b = pop(vm);
                int a = pop(vm);
                push(vm, a * b);
                break;
            }
            
            case DIV: {
                int b = pop(vm);
                int a = pop(vm);
                if (b == 0) {
                    fprintf(stderr, "Division by zero\n");
                    exit(1);
                }
                push(vm, a / b);
                break;
            }
            
            case EQ: {
                int b = pop(vm);
                int a = pop(vm);
                push(vm, a == b ? 1 : 0);
                break;
            }
            
            case LT: {
                int b = pop(vm);
                int a = pop(vm);
                push(vm, a < b ? 1 : 0);
                break;
            }
            
            case GT: {
                int b = pop(vm);
                int a = pop(vm);
                push(vm, a > b ? 1 : 0);
                break;
            }
            
            case MOD: {
                int b = pop(vm);
                int a = pop(vm);
                if (b == 0) {
                    fprintf(stderr, "Modulo by zero\n");
                    exit(1);
                }
                push(vm, a % b);
                break;
            }
            
            case LE: {
                int b = pop(vm);
                int a = pop(vm);
                push(vm, a <= b ? 1 : 0);
                break;
            }
            
            case GE: {
                int b = pop(vm);
                int a = pop(vm);
                push(vm, a >= b ? 1 : 0);
                break;
            }
            
            case DUP: {
                if (operand >= vm->sp) {
                    fprintf(stderr, "DUP: Stack offset out of range\n");
                    exit(1);
                }
                int value = vm->stack[vm->sp - 1 - operand];
                push(vm, value);
                break;
            }

            case SWAPDUP: {
                if (operand >= vm->sp) {
                    fprintf(stderr, "SWAPDUP: Stack offset out of range\n");
                    exit(1);
                }
                int top = vm->stack[vm->sp - 1];
                int offset_value = vm->stack[vm->sp - 1 - operand];
                vm->stack[vm->sp - 1] = offset_value;
                vm->stack[vm->sp - 1 - operand] = top;
                push(vm, vm->stack[vm->sp - 1]); // Duplicate the new top
                break;
            }

            case JMPT: {
                int cond = pop(vm);
                if (cond) {
                    vm->pc = operand;
                }
                break;
            }
            
            case JMP:
                vm->pc = operand;
                break;
                
            case JMPF: {
                int cond = pop(vm);
                if (!cond) {
                    vm->pc = operand;
                }
                break;
            }
            
            case LOAD:
                push(vm, vm->memory[operand]);
                break;
                
            case STORE:
                vm->memory[operand] = pop(vm);
                break;
                
            case ARRAY: {
                int size = pop(vm);
                if (vm->array_count >= MAX_ARRAYS) {
                    fprintf(stderr, "Too many arrays\n");
                    exit(1);
                }
                Array* arr = &vm->arrays[vm->array_count];
                arr->data = malloc(size * sizeof(int));
                arr->size = size;
                for (int i = 0; i < size; i++) {
                    arr->data[i] = 0;
                }
                push(vm, vm->array_count);  // Push array ID
                vm->array_count++;
                break;
            }
            
            case ALOAD: {
                int index = pop(vm);
                int array_id = pop(vm);  // Pop array ID instead of peeking
                if (array_id < 0 || array_id >= vm->array_count) {
                    fprintf(stderr, "Invalid array ID: %d\n", array_id);
                    exit(1);
                }
                Array* arr = &vm->arrays[array_id];
                if (index < 0 || index >= arr->size) {
                    fprintf(stderr, "Array index out of bounds: %d (size: %d)\n", index, arr->size);
                    exit(1);
                }
                push(vm, arr->data[index]);
                break;
            }
            
            case ASTORE: {
                int value = pop(vm);
                int index = pop(vm);
                int array_id = pop(vm);
                if (array_id < 0 || array_id >= vm->array_count) {
                    fprintf(stderr, "Invalid array ID: %d\n", array_id);
                    exit(1);
                }
                Array* arr = &vm->arrays[array_id];
                if (index < 0 || index >= arr->size) {
                    fprintf(stderr, "Array index out of bounds: %d (size: %d)\n", 
                            index, arr->size);
                    exit(1);
                }
                arr->data[index] = value;
                push(vm, array_id);  // Push array ID back for chained operations
                break;
            }
            
            default:
                fprintf(stderr, "Unknown opcode: %d\n", opcode);
                exit(1);
        }
    }
}

void print_bytecode(unsigned char* bytecode, int size) {
    printf("Bytecode (%d bytes):\n", size);
    for (int i = 0; i < size; i += 2) {
        unsigned char opcode = bytecode[i];
        unsigned char operand = bytecode[i+1];
        printf("  %04d: %03d %03d\n", i, opcode, operand);
    }
    printf("\n");
}

int main(int argc, char** argv) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <bytecode_file>\n", argv[0]);
        return 1;
    }
    
    FILE* file = fopen(argv[1], "rb");
    if (!file) {
        fprintf(stderr, "Cannot open file: %s\n", argv[1]);
        return 1;
    }
    
    // Read bytecode from file
    fseek(file, 0, SEEK_END);
    long size = ftell(file);
    fseek(file, 0, SEEK_SET);
    
    unsigned char* bytecode = malloc(size);
    fread(bytecode, 1, size, file);
    fclose(file);
    
    print_bytecode(bytecode, size);
    
    // Execute bytecode
    VM vm;
    vm_init(&vm);
    printf("Executing bytecode...\n");
    execute(&vm, bytecode, size);
    
    // Print final result
    printf("\nExecution complete\n");
    if (vm.sp > 0) {
        printf("Final stack top: %d\n", vm.stack[vm.sp - 1]);
    } else {
        printf("Stack is empty\n");
    }
    
    // Clean up
    free(bytecode);
    for (int i = 0; i < vm.array_count; i++) {
        free(vm.arrays[i].data);
    }
    
    return 0;
}