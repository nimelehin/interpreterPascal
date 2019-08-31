from Interpreter.interpret import Interpret
from Interpreter.Parser.parse import Parser
from Interpreter.types import Type
from Interpreter.token import Token

def run():
    str = input()
    kek = Interpret(Parser(str))
    print(kek.interpret())