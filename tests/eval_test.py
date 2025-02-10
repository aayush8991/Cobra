"""
Tests eval.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from eval import e
from tree import BinOp
from lexer import IntToken, FloatToken, StringToken, BoolToken

def test_number():
    tree = IntToken(42)
    result = e(tree)
    assert result.v == 42
    assert isinstance(result, IntToken)

def test_addition():
    tree = BinOp("+", IntToken(3), IntToken(5))
    result = e(tree)
    assert result.v == 8
    assert isinstance(result, IntToken)

def test_multiplication():
    tree = BinOp("*", IntToken(3), IntToken(5))
    result = e(tree)
    assert result.v == 15
    assert isinstance(result, IntToken)

def test_float_operation():
    tree = BinOp("+", FloatToken(2.5), IntToken(3))
    result = e(tree)
    assert result.v == 5.5
    assert isinstance(result, FloatToken)

def test_string_concatenation():
    tree = BinOp("+", StringToken("Hello "), StringToken("World"))
    result = e(tree)
    assert result.v == "Hello World"
    assert isinstance(result, StringToken)

def test_string_repetition():
    tree = BinOp("*", StringToken("Hi"), IntToken(3))
    result = e(tree)
    assert result.v == "HiHiHi"
    assert isinstance(result, StringToken)

def test_nested_operations():
    tree = BinOp("*", BinOp("+", IntToken(2), IntToken(3)), IntToken(4))
    result = e(tree)
    assert result.v == 20
    assert isinstance(result, IntToken)
