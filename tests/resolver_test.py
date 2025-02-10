import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tree import *
from lexer import *
from resolver import resolve

def test_simple_let():
    env = []
    ast = Let(Var("x", None), IntToken(5), BinOp("+", Var("x", None), IntToken(3)))
    expected = Let(Var("x", 0), IntToken(5), BinOp("+", Var("x", 0), IntToken(3)))
    assert resolve(ast, env) == expected

def test_nested_let():
    env = []
    ast = Let(Var("x", None), IntToken(5),
              Let(Var("y", None), IntToken(10),
                  BinOp("+", Var("x", None), Var("y", None))))
    expected = Let(Var("x", 0), IntToken(5),
                   Let(Var("y", 0), IntToken(10),
                       BinOp("+", Var("x", 1), Var("y", 0))))
    assert resolve(ast, env) == expected

def test_variable_not_found():
    env = []
    ast = Var("z", None)
    with pytest.raises(ValueError, match="Unbound variable: z"):
        resolve(ast, env)

def test_function():
    env = []
    ast = Fun("f", Var("x", None), "int", BinOp("*", Var("x", None), IntToken(2)))
    expected = Fun("f", Var("x", 0), "int", BinOp("*", Var("x", 0), IntToken(2)))
    assert resolve(ast, env) == expected

def test_function_call():
    env = [("x", None)]
    ast = Call("f", Var("x", None))
    expected = Call("f", Var("x", 0))
    assert resolve(ast, env) == expected

def test_if_expression():
    env = [("x", None)]
    ast = If(BinOp(">", Var("x", None), IntToken(0)),
             IntToken(1),
             IntToken(0))
    expected = If(BinOp(">", Var("x", 0), IntToken(0)),
                  IntToken(1),
                  IntToken(0))
    assert resolve(ast, env) == expected

def test_while_loop():
    env = [("x", None)]
    ast = While(BinOp("<", Var("x", None), IntToken(10)),
                BinOp("+", Var("x", None), IntToken(1)))
    expected = While(BinOp("<", Var("x", 0), IntToken(10)),
                     BinOp("+", Var("x", 0), IntToken(1)))
    assert resolve(ast, env) == expected
    