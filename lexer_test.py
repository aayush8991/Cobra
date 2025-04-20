from lexer import IntToken, FloatToken, StringToken, BoolToken

def test_int_token():
    token = IntToken(42)
    assert token.v == 42
    assert isinstance(token, IntToken)

def test_float_token():
    token = FloatToken(3.14)
    assert token.v == 3.14
    assert isinstance(token, FloatToken)

def test_string_token():
    token = StringToken("Hello")
    assert token.v == "Hello"
    assert isinstance(token, StringToken)

def test_bool_token():
    token_true = BoolToken(True)
    token_false = BoolToken(False)
    assert token_true.v is True
    assert token_false.v is False
    assert isinstance(token_true, BoolToken)
    assert isinstance(token_false, BoolToken)
