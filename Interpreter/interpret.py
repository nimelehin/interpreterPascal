from Interpreter.TreeComponents.visitor import Visitor

class Interpret(Visitor):
    def __init__(self, parser):
        self.parser = parser

    def interpret(self):
        tree = self.parser.expr()
        print(tree)
        return self.visit(tree) 

