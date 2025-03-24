# 📖 Getting Started with Cobra
Welcome to Cobra, a powerful and expressive programming language that combines dynamic typing, lexical scoping, first-class functions, and structured syntax. This guide will help you write your first program and understand the core features of the language.

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

# 👋 Your First Program
Lets now write our first program in Cobra 🐍.
```
let hello be "Hello, " in
    let world be "World!" in
        hello + world
    end
end
```

The code to be run needs to be added in code.txt and run from the main.py
The flow can be observed using the AST,
![alt text](ast_tree.png)
