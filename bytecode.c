#include <stdio.h>
#include <stdint.h>
#include "opcode.h"

int execute(uint8_t *insns)
{
  size_t ip = 0;
  int operand[100], top = 0;
#define PUSH(x) (operand[top++] = x)
#define POP(x) (operand[--top])	

  int l, r;
  while (1) {
    switch (insns[ip]) {
    case HALT: goto end;
    case NOP: break;
    case PUSH:
   PUSH(insns[ip+1]); break;
    case ADD:
   r = POP(); l = POP(); PUSH(l+r); break;
    case SUB:
   r = POP(); l = POP(); PUSH(l-r); break;
    case MUL:
   r = POP(); l = POP(); PUSH(l*r); break;
    case NEG:
   l = POP(); PUSH(-l); break;
    }
    ip += 2; // No control-flow.
  }
 end:
  return POP();
#undef PUSH
#undef POP
}

// <<instruction-def>>
// <<execute-def>>
int main()
{
    uint8_t insns[] = {
   PUSH, 2,
   PUSH, 3,
   ADD , 0, // 0 is ignored.
   PUSH, 5,
   MUL , 0,
   HALT, 0,
    };
    printf("%d\n", execute(insns));
    return 0;
}