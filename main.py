from parser import parse
from evaluator import e

if __name__ == "__main__":
    expression = '2 + 5 * 6 / 2'
    result = e(parse(expression))
    print(f"Result: {result}")
