import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser import parse
from tree import Number, BinOp, IntToken

def test_single_number():
    tree = parse("42")
    assert isinstance(tree, Number)
    assert tree.v.v == 42

def test_addition():
    tree = parse("3 + 5")
    assert isinstance(tree, BinOp)
    assert tree.op == "+"
    assert tree.left.v.v == 3
    assert tree.right.v.v == 5

def test_nested_expression():
    tree = parse("(1 + 2) * 4")
    assert isinstance(tree, BinOp)
    assert tree.op == "*"
    assert isinstance(tree.left, BinOp)
    assert tree.left.op == "+"
    assert tree.left.left.v.v == 1
    assert tree.left.right.v.v == 2
    assert tree.right.v.v == 4
