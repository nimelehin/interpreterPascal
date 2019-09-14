from Interpreter.interpret import Interpret
from Interpreter.Parser.parse import Parser
from Interpreter.types import Type
from Interpreter.token import Token

def run(filename):
    inter = Interpret(Parser())
    while True:
        str = input()
        inter.parser.set_code_line(str)
        print(inter.interpret())