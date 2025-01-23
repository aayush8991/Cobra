from dataclasses import dataclass

class ParseError(Exception):
    """Exception raised for errors in the parsing process."""
    pass

class Token:
    pass

@dataclass
class NumberToken(Token):
    v: str

@dataclass
class OperatorToken(Token):
    o: str

@dataclass
class KeywordToken(Token):
    w: str
