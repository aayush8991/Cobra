from collections.abc import Iterator
from token_class import *

def lex(s: str) -> Iterator[Token]:
    i = 0
    while True:
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
            # # XXX: Should check here whether we got a valid keyword.
            yield KeywordToken(t)
        if s[i].isdigit():
            t = s[i]
            i = i + 1
            while i < len(s) and (s[i].isdigit() or s[i] == '.'):
                if s[i] == '.' and '.' in t:
                    break                       # Ensure only one decimal point
                t = t + s[i]
                i = i + 1
            yield NumberToken(t)
        else:
            match t := s[i]:
                case '+' | '*' | '-' | '/' | '^' | '(' | ')' | '<' | '>' | '{' | '}':
                    i = i + 1
                    yield OperatorToken(t)
                case '=':
                    if i + 1 < len(s) and s[i + 1] == '=':
                        i = i + 2
                        yield OperatorToken('==')