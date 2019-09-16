from Interpreter.interpret import Interpret
from Interpreter.Parser.parse import Parser
from Interpreter.types import Type
from Interpreter.token import Token

def run(filename):

    code = []

    file = open(filename, "r") 
    for line in file: 
        line = line.replace('\n', '')
        if len(line) > 0:
            code.append(line)

    inter = Interpret(Parser())
    inter.parser.set_code_lines(code)
    print(inter.interpret())