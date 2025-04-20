from parser import parse
from tree import BinOp

def test_addition():
    tree = parse("3 + 5")
    assert isinstance(tree, BinOp)
    assert tree.op == "+"
    assert tree.left.v == 3
    assert tree.right.v == 5

def test_nested_expression():
    tree = parse("(1 + 2) * 4")
    assert isinstance(tree, BinOp)
    assert tree.op == "*"
    assert isinstance(tree.left, BinOp)
    assert tree.left.op == "+"
    assert tree.left.left.v == 1
    assert tree.left.right.v == 2
    assert tree.right.v == 4
