import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest

from tree import *
from lexer import *
from resolver import resolve

def test_simple_let():
    ast = Let(Var("x", None), IntToken(5), BinOp("+", Var("x", None), IntToken(3)))
    expected = Let(Var("x", 0), IntToken(5), BinOp("+", Var("x", 0), IntToken(3)))
    assert resolve(ast) == expected

def test_nested_let():
    ast = Let(Var("x", None), IntToken(5),
              Let(Var("y", None), IntToken(10),
                  BinOp("+", Var("x", None), Var("y", None))))
    expected = Let(Var("x", 0), IntToken(5),
                   Let(Var("y", 0), IntToken(10),
                       BinOp("+", Var("x", 1), Var("y", 0))))
    assert resolve(ast) == expected

def test_variable_not_found():
    ast = Var("z", None)
    with pytest.raises(ValueError, match="Unbound variable: z"):
        resolve(ast)

def test_function():
    ast = Fun("f", Var("x", None), "int", BinOp("*", Var("x", None), IntToken(2)))
    expected = Fun("f", Var("x", 0), "int", BinOp("*", Var("x", 0), IntToken(2)))
    assert resolve(ast) == expected

def test_function_call():
    ast = Let(Var("x", None), IntToken(5),
              Call("f", Var("x", None)))
    expected = Let(Var("x", 0), IntToken(5),
                   Call("f", Var("x", 0)))
    assert resolve(ast) == expected

def test_if_expression():
    ast = Let(Var("x", None), IntToken(5),
              If(BinOp(">", Var("x", None), IntToken(0)),
                   IntToken(1),
                   IntToken(0)))
    expected = Let(Var("x", 0), IntToken(5),
                   If(BinOp(">", Var("x", 0), IntToken(0)),
                        IntToken(1),
                        IntToken(0)))
    assert resolve(ast) == expected

def test_while_loop():
    ast = Let(Var("x", None), IntToken(5),
              While(BinOp("<", Var("x", None), IntToken(10)),
                    BinOp("+", Var("x", None), IntToken(1))))
    expected = Let(Var("x", 0), IntToken(5),
                   While(BinOp("<", Var("x", 0), IntToken(10)),
                         BinOp("+", Var("x", 0), IntToken(1))))
    assert resolve(ast) == expected
