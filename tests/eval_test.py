import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tree import e
from tree import Number, BinOp
from lexer import IntToken, FloatToken, StringToken, BoolToken

def test_number():
    tree = Number(IntToken(42))
    result = e(tree)
    assert result.v == 42
    assert isinstance(result, IntToken)

def test_addition():
    tree = BinOp("+", Number(IntToken(3)), Number(IntToken(5)))
    result = e(tree)
    assert result.v == 8
    assert isinstance(result, IntToken)

def test_multiplication():
    tree = BinOp("*", Number(IntToken(3)), Number(IntToken(5)))
    result = e(tree)
    assert result.v == 15
    assert isinstance(result, IntToken)

def test_float_operation():
    tree = BinOp("+", Number(FloatToken(2.5)), Number(IntToken(3)))
    result = e(tree)
    assert result.v == 5.5
    assert isinstance(result, FloatToken)

def test_string_concatenation():
    tree = BinOp("+", Number(StringToken("Hello ")), Number(StringToken("World")))
    result = e(tree)
    assert result.v == "Hello World"
    assert isinstance(result, StringToken)

def test_string_repetition():
    tree = BinOp("*", Number(StringToken("Hi")), Number(IntToken(3)))
    result = e(tree)
    assert result.v == "HiHiHi"
    assert isinstance(result, StringToken)

def test_nested_operations():
    tree = BinOp("*", BinOp("+", Number(IntToken(2)), Number(IntToken(3))), Number(IntToken(4)))
    result = e(tree)
    assert result.v == 20
    assert isinstance(result, IntToken)
