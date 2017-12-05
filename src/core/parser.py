"""Parse a file and run it"""
import core.environment

def lex(file: str, comment: str) -> list:
    """Parse source file"""
    source = open(file)
    tokens = []
    for line in source:
        for ch in line:
            if ch == comment:
                break
            tokens += ch
    return tokens

def parse(tokens: list, length: int, size: int, wrapping: bool, end_of_loop: int):
    env = core.environment.Environment(length, size, wrapping, end_of_loop)
    env.parse(tokens)