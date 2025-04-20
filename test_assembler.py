import unittest
from assembler import codegen
from lexer import IntToken
from tree import Var, Let, BinOp, While, Assign, Array, ArrayIndex, ArrayAssign, Fun, Call
from decimal import Decimal

class TestAssembler(unittest.TestCase):
    def test_simple_arithmetic(self):
        expr = BinOp(op="+", left=IntToken(v=Decimal("2")), right=IntToken(v=Decimal("3")))
        bytecode = codegen(expr)
        expected = bytearray([1, 2, 1, 3, 3, 0])  # PUSH 2, PUSH 3, ADD, HALT
        self.assertEqual(bytecode, expected)

    def test_variable_assignment(self):
        expr = Let(
            v=Var(v="x", i=None),
            e=IntToken(v=Decimal("42")),
            f=Var(v="x", i=None)
        )
        bytecode = codegen(expr)
        expected = bytearray([1, 42, 14, 0, 13, 0, 0])  # PUSH 42, STORE 0, LOAD 0, HALT
        self.assertEqual(bytecode, expected)

    def test_while_loop(self):
        expr = Let(
            v=Var(v="i", i=None),
            e=IntToken(v=Decimal("0")),
            f=While(
                condition=BinOp(op="<", left=Var(v="i", i=None), right=IntToken(v=Decimal("5"))),
                body=[
                    Assign(
                        var=Var(v="i", i=None),
                        expr=BinOp(op="+", left=Var(v="i", i=None), right=IntToken(v=Decimal("1")))
                    )
                ]
            )
        )
        bytecode = codegen(expr)
        expected = bytearray([
            1, 0, 14, 0,  # PUSH 0, STORE 0
            13, 0, 1, 5, 9,  # LOAD 0, PUSH 5, LT
            12, 20,  # JMPF to end
            13, 0, 1, 1, 3, 14, 0,  # LOAD 0, PUSH 1, ADD, STORE 0
            11, 4,  # JMP to start
            0  # HALT
        ])
        self.assertEqual(bytecode, expected)

    def test_array_operations(self):
        expr = Let(
            v=Var(v="arr", i=None),
            e=Array(elements=[IntToken(v=Decimal("1")), IntToken(v=Decimal("2")), IntToken(v=Decimal("3"))]),
            f=ArrayIndex(array=Var(v="arr", i=None), index=IntToken(v=Decimal("1")))
        )
        bytecode = codegen(expr)
        expected = bytearray([
            1, 3, 17,  # PUSH 3, ARRAY
            1, 1, 1, 2, 1, 3,  # PUSH 1, PUSH 2, PUSH 3
            14, 0,  # STORE 0
            13, 0, 1, 1, 18,  # LOAD 0, PUSH 1, ALOAD
            0  # HALT
        ])
        self.assertEqual(bytecode, expected)

    def test_function_definition_and_call(self):
        expr = Let(
            v=Var(v="sum", i=None),
            e=Fun(
                parameters=[Var(v="a", i=None), Var(v="b", i=None)],
                body=BinOp(op="+", left=Var(v="a", i=None), right=Var(v="b", i=None))
            ),
            f=Call(
                func=Var(v="sum", i=None),
                args=[IntToken(v=Decimal("2")), IntToken(v=Decimal("3"))]
            )
        )
        bytecode = codegen(expr)
        expected = bytearray([
            11, 8,  # JMP to skip function
            13, 0, 13, 1, 3, 16,  # Function body: LOAD 0, LOAD 1, ADD, RET
            1, 2,  # PUSH function address
            14, 0,  # STORE 0
            1, 2, 1, 3,  # PUSH 2, PUSH 3
            1, 2,  # PUSH number of arguments
            13, 0, 15,  # LOAD 0, CALL
            0  # HALT
        ])
        self.assertEqual(bytecode, expected)

    def test_negative_and_subtraction(self):
        expr = BinOp(op="-", left=IntToken(v=Decimal("10")), right=IntToken(v=Decimal("3")))
        bytecode = codegen(expr)
        expected = bytearray([1, 10, 1, 3, 4, 0])  # PUSH 10, PUSH 3, SUB, HALT
        self.assertEqual(bytecode, expected)

    def test_array_assignment_and_indexing(self):
        expr = Let(
            v=Var(v="arr", i=None),
            e=Array(elements=[IntToken(v=Decimal("0")), IntToken(v=Decimal("0")), IntToken(v=Decimal("0"))]),
            f=Let(
                v=Var(v="tmp", i=None),
                e=ArrayAssign(
                    array=Var(v="arr", i=None),
                    index=IntToken(v=Decimal("1")),
                    value=IntToken(v=Decimal("42"))
                ),
                f=ArrayIndex(array=Var(v="arr", i=None), index=IntToken(v=Decimal("1")))
            )
        )
        bytecode = codegen(expr)
        expected = bytearray([
            1, 3, 17,  # PUSH 3, ARRAY
            1, 0, 1, 0, 1, 0,  # PUSH 0, PUSH 0, PUSH 0
            14, 0,  # STORE 0
            13, 0, 1, 1, 1, 42, 19,  # LOAD 0, PUSH 1, PUSH 42, ASTORE
            14, 1,  # STORE 1
            13, 0, 1, 1, 18,  # LOAD 0, PUSH 1, ALOAD
            0  # HALT
        ])
        self.assertEqual(bytecode, expected)

    def test_function_returning_constant(self):
        expr = Let(
            v=Var(v="five", i=None),
            e=Fun(parameters=[], body=IntToken(v=Decimal("5"))),
            f=Call(func=Var(v="five", i=None), args=[])
        )
        bytecode = codegen(expr)
        expected = bytearray([
            11, 5,  # JMP over function body
            1, 5, 16,  # Function body: PUSH 5, RET
            1, 2,  # PUSH function address
            14, 0,  # STORE 0
            1, 0,  # PUSH number of args
            13, 0, 15,  # LOAD 0, CALL
            0  # HALT
        ])
        self.assertEqual(bytecode, expected)

    def test_function_using_variable(self):
        expr = Let(
            v=Var(v="x", i=None),
            e=IntToken(v=Decimal("7")),
            f=Let(
                v=Var(v="f", i=None),
                e=Fun(parameters=[], body=Var(v="x", i=None)),
                f=Call(func=Var(v="f", i=None), args=[])
            )
        )
        bytecode = codegen(expr)
        expected = bytearray([
            1, 7, 14, 0,  # PUSH 7, STORE 0 (x)
            11, 9,       # JMP over function
            13, 0, 16,    # LOAD 0, RET (uses x from outer scope)
            1, 6, 14, 1,  # PUSH 6 (func addr), STORE 1 (f)
            1, 0, 13, 1, 15,  # PUSH 0, LOAD f, CALL
            0  # HALT
        ])
        self.assertEqual(bytecode, expected)

    def test_nested_function_calls(self):
        expr = Let(
            v=Var(v="add", i=None),
            e=Fun(
                parameters=[Var(v="a", i=None), Var(v="b", i=None)],
                body=BinOp(op="+", left=Var(v="a", i=None), right=Var(v="b", i=None))
            ),
            f=Let(
                v=Var(v="result", i=None),
                e=Call(func=Var(v="add", i=None), args=[IntToken(v=Decimal("1")), IntToken(v=Decimal("2"))]),
                f=Call(func=Var(v="add", i=None), args=[Var(v="result", i=None), IntToken(v=Decimal("3"))])
            )
        )
        bytecode = codegen(expr)
        expected = bytearray([
            11, 8,               # JMP over func
            13, 0, 13, 1, 3, 16,  # LOAD a, LOAD b, ADD, RET
            1, 2, 14, 0,         # PUSH 10, STORE add
            1, 1, 1, 2, 1, 2, 13, 0, 15,  # PUSH args, PUSH n, LOAD add, CALL
            14, 1,                # STORE result
            13, 1, 1, 3, 1, 2, 13, 0, 15,  # LOAD result, PUSH 3, PUSH 2, LOAD add, CALL
            0  # HALT
        ])
        self.assertEqual(bytecode, expected)

if __name__ == "__main__":
    unittest.main()