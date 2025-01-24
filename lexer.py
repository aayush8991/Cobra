from dataclasses import dataclass
from collections.abc import Iterator

class ParseError(Exception):
    """Exception raised for errors in the parsing process."""
    pass

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
class BoolToken(Token):
    v: bool

@dataclass
class StringToken(Token):
    v: str
    
@dataclass
class OperatorToken(Token):
    o: str

keywords = {"if", "then", "else"}

def lex(s: str) -> Iterator[Token]:
    i = 0
    while True:
        # Skip whitespace
        while i < len(s) and s[i].isspace():
            i = i + 1

        if i >= len(s):
            return

        if s[i].isalpha():
            t = s[i]
            i = i + 1
            while i < len(s) and s[i].isalpha():
                t = t + s[i]
                i = i + 1
            if t in keywords:
                yield KeywordToken(t)
            else:
                raise ValueError(f"Unexpected keyword: {t}")

        elif s[i].isdigit():
            t = s[i]
            i = i + 1
            while i < len(s) and (s[i].isdigit() or s[i] == '.'):
                if s[i] == '.' and '.' in t:  # Ensure only one decimal point
                    break
                t = t + s[i]
                i = i + 1
            if '.' in t:
                yield FloatToken(float(t))
            else:
                yield IntToken(int(t))

        elif s[i] == '"':
            i += 1
            start = i
            while i < len(s) and s[i] != '"':
                i += 1
            if i >= len(s):
                raise ValueError("Unterminated string literal")
            yield StringToken(s[start:i])
            i += 1

        else:
            match t := s[i]:
                case '+' | '*' | '-' | '/' | '^' | '(' | ')':
                    i = i + 1
                    yield OperatorToken(t)
