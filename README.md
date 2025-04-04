![image](https://github.com/user-attachments/assets/44620a70-5440-4163-9468-5ddd88e3fe1d)

# 📖 Getting Started with Cobra
Welcome to Cobra, a powerful and expressive programming language that combines dynamic typing, lexical scoping, first-class functions, and structured syntax. This guide will help you write your first program and understand the core features of the language.

# Progress Overview

| Component                  | Status                     |
|----------------------------|----------------------------|
| Lexer                      | ✅ Completed               |
| Parser                     | ✅ Completed               |
| AST Generation             | ✅ Completed               |
| Type Checking              | ⏳ Partial Implementation  |
| Bytecode Generation (C)    | ✅ Completed               |
| Virtual Machine            | ⏳ In Progress             |
| Standard Library           | ⏳ Basic Features Implemented |


# Components Implemented

### Calculator with Arithmetic Operations
- Supports basic arithmetic operations: `+`, `-`, `*`, `/`.
- Parentheses for precedence handling.
- Uses Abstract Syntax Trees (ASTs) for efficient evaluation and optimization.
#### Example:
```plaintext
let a be 10 in
    let b be 5 in
        let result be (a + b) * (a - b) / b in
            print(result)
        end
    end
end
```

### Conditionals
- Implements `if-else` statements.
- Supports boolean expressions (`x > 5`, `y == 10`).
- Short-circuit evaluation for `&&` and `||`.
#### Example:
```plaintext
let a be 10 in
    if {a > 5 and a < 15} then
        print("a is between 5 and 15")
    else
        print("a is not between 5 and 15")
    end
end
```
### Variables
- Supports variable declaration and assignment (`x = 10`).
- Symbol table for managing names, types, and memory locations.
- Currently supports global variables, with local scoping planned.
#### Example:
```plaintext
let x be 10 in
    let y be x + 5 in
        print(y)
    end
end
```
### Functions (Value-Returning)
- Basic function definitions and calls implemented.
- Supports single-parameter functions with return values.
- Function table tracks names, parameters, and return types.
#### Example:
```plaintext
let square be fun(x) is {
    x * x
} in
    print(square(5))
end
```
### Loops
- **While Loop** implemented.
- Evaluates loop conditions and executes body until condition is `false`.
- Enables repetitive task execution.
#### Example:
```plaintext
let i be 0 in
    let sum be 0 in
        while {i < 5} do
            sum := sum + i
            i := i + 1
        end;
        print(sum)
    end
end
```
### Lexical Scoping
- Symbol table supports hierarchical scopes.
- New scopes pushed onto a stack when entering blocks/functions.
- Variables resolved by traversing the scope chain.
#### Example:
```plaintext
let x be 5 in
    let f be fun(y) is {x} in
        let g be fun(z) is {let x be 6 in f(z) end} in
            g(0)
        end
    end
end
```

### Arrays
- Implemented support for arrays.
- Arrays can be indexed and iterated over using loops.
#### Example:
```plaintext
let arr be [1, 2, 3, 4, 5] in
    let i be 0 in
        while {i < 5} do
            {print(arr[i])}
            {i := i + 1}
        end
    end
end
```
### Bytecode Generation
- Optimized AST-to-bytecode translation.
- Efficient bytecode execution for arithmetic, conditionals, loops, and functions.


# Basic Functionalities
## 🔢 Variables and Data Types
You don’t have to declare variable types explicitly.
```
let a be 0 in main end
```

## 🧮 Functions
```
fun(<arg>) is { body } 
```

## 🗂️ Scope and Lexical Scoping
![alt text](image.png)

# 🔄 Control Flow
```
if {a < b} then
    {"a is less than b"}
else
    {"a is not less than b"}
end
```

# 🔁 Loops
Loops allow repetitive execution of code. Cobra supports only while loops.
```
while {condition} do
    {body}
end
```


# Language Features

### First-Class Functions
- Functions can be assigned to variables, passed as arguments, and returned from other functions.
- Enables higher-order functions and modular programming.
#### Example:
```plaintext
let apply be fun(f, x) is { f(x) } in
    let double be fun(n) is { n * 2 } in
        apply(double, 5)
    end
end
```

### Lexical Scoping (Static Scope Resolution)
- Variables are resolved based on their position in the source code.
- Inner functions can access outer function variables but cannot modify them unless explicitly declared.

### Dynamic Typing
- Variables do not require explicit type declarations.
- Types can change during execution for flexibility.

### Scope Definition Using `()` and `{}`
- **Parentheses `()`**: Used for function arguments, conditionals, and loops.
- **Curly Braces `{}`**: Define explicit code blocks for structured programming.


# 👋 Your First Program
Lets now write our first program in Cobra 🐍.
```
print("Hello World")
```


## Test Coverage

### Ease of Running Tests
- `run_tests.sh` runs all test cases.
- Uses `pytest` for frontend tests and `CUnit` for backend bytecode tests.

### Coverage & Quality
- **Lexer & Parser**: High coverage with various input cases.
- **Type System**: Needs more edge case tests.
- **Bytecode Execution**: Basic arithmetic and control flow tested.
- **Error Handling**: Needs dedicated tests for syntax errors and runtime exceptions.


# How to run
The code to be run needs to be added in code.txt and run from the main.py
The flow can be observed using the AST,
![alt text](ast_tree.png)


# Team Roles and Responsibilities

| Component                      | Responsible Members  | Description  |
|--------------------------------|----------------------|--------------|
| **Lexical Analysis (Lexer)**   | Aashmun & Dewansh   | Tokenizes source code. |
| **Parsing (Syntax Analysis)**  | Aashmun & Aayush    | Converts tokens to AST. |
| **Intermediate Code (IR)**     | Aayush & Bhoumik    | Translates AST to IR. |
| **Optimization**               | Aayush & Dewansh    | Improves performance. |
| **Code Generation (Backend)**  | Aayush & Dewansh    | Converts IR to bytecode/machine code. |
| **Semantic Analysis & Type Checking** | Aashmun & Bhoumik | Ensures type safety and scope rules. |
| **REPL & Execution**           | Yet to be completed | Interactive Read-Eval-Print Loop. |
| **Testing & Debugging**        | All Members         | Unit tests, integration tests. |
| **Documentation & Packaging**  | Aashmun & Aayush    | User-friendly documentation and packaging. |

<<<<<<< HEAD

<iframe src="https://docs.google.com/presentation/d/1M_ANAZm4amV9q1QWfF7wMY5ip1FoqRIlDIwmkreqP8w/edit#slide=id.p" width="800" height="450"></iframe>

=======
>>>>>>> e2ca46e6a2f935afee076aa4401c0fb1fd9ce6e4
#
This documentation will be updated as development progresses. 🚀
