from Interpreter.TreeComponents.visitor import Visitor

class Interpret(Visitor):
    def __init__(self, parser):
        Visitor.__init__(self)
        self.parser = parser

    def interpret(self):
        tree = self.parser.assign()
        print(tree)
        return self.visit(tree) 

