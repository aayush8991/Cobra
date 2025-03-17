import sys
from parser import parse
from eval import e
from resolver import resolve

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <code_file>")
        return

    code_file = sys.argv[1]
    try:
        with open(code_file, "r") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{code_file}' not found.")
        return

    ast = parse(code)
    abt = resolve(ast)
    result = e(abt)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()