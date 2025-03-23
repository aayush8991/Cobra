from dataclasses import dataclass
from collections.abc import Iterator
from decimal import Decimal

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
    v: Decimal

@dataclass
class FloatToken(Token):
    v: Decimal

@dataclass
class BoolToken(Token):
    v: bool

@dataclass
class StringToken(Token):
    v: str
    
@dataclass
class OperatorToken(Token):
    o: str

@dataclass
class VariableToken(Token):
    v: str

keywords = ["if", "then", "else", "end", "let", "in", "be", "while", "do", "fun", "is"]

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
            elif t == "true":
                yield BoolToken(True)
            elif t == "false":
                yield BoolToken(False)
            else:
                yield VariableToken(t)

        elif s[i].isdigit():
            t = s[i]
            i = i + 1
            while i < len(s) and (s[i].isdigit() or s[i] == '.'):
                if s[i] == '.' and '.' in t:  # Ensure only one decimal point
                    break
                t = t + s[i]
                i = i + 1
            if '.' in t:
                yield FloatToken(Decimal(t))
            else:
                yield IntToken(Decimal(t))

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
                case '+' | '*' | '-' | '/' | '^' | '(' | ')' | '<' | '>' | '{' | '}' | ',' | '[' | ']':
                    i = i + 1
                    yield OperatorToken(t)
                case '=':
                    if i + 1 < len(s) and s[i + 1] == '=':
                        i = i + 2
                        yield OperatorToken('==')
                case '!':
                    if i + 1 < len(s) and s[i + 1] == '=':
                        i = i + 2
                        yield OperatorToken('!=')
                case ':':
                    if i + 1 < len(s) and s[i + 1] == '=':
                        i = i + 2
                        yield OperatorToken(':=')  
