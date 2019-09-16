class Node:
    
    class Basic():
        def __str__(self):
            return "type: {0}".format(self.type)
    
    class Number(Basic):
        def __init__(self, token):
            self.value = token.value
            self.type = token.type

    class Var(Basic):
        def __init__(self, token):
            self.value = token.value
            self.type = token.type

    class BinaryOperation(Basic):
        def __init__(self, a, b, token):
            self.left = a
            self.right = b
            self.value = token.value
            self.type = token.type

    class NoOperation(Basic):
        def __init__(self):
            self.type = 'NoOperation'

    class Compound(Basic):
        def __init__(self, children = []):
            self.children = children
            self.type = 'Compound'

    class UnaryOperation(Basic):
        def __init__(self, a, token):
            self.left = a
            self.value = token.value
            self.type = token.type

    class VarsDeclatrations(Basic):
        def __init__(self, vars, vars_type):
            self.vars = vars
            self.vars_type = vars_type
            self.type = 'VarsDeclatrations'

    class Program(Basic):
        def __init__(self, name, vars_declarations, main):
            self.name = name
            self.vars_declarations = vars_declarations
            self.main = main
            self.type = 'Program'