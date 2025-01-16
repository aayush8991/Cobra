class Token:
    pass

@dataclass
class KeywordToken(Token):
    v: str
    
@dataclass
class IntToken(Token):
    v: int

@dataclass
class FloatToken(Token):
    v: float

@dataclass
class StringToken(Token):
    v: str
    
@dataclass
class OperatorToken(Token):
    o: str