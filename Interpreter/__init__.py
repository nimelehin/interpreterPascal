from Interpreter.Lexer.lexer import Lexer
from Interpreter.types import Type
from Interpreter.token import Token

def run():
    str = input()
    lexer = Lexer(str)
    lx = Token('', '')
    while lx.type != Type.Special.EOF:
        lx = lexer.get_next_token()
        print(lx)