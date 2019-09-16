from Interpreter.types import Type

class NodeVisitor():
    def visit(self, node):
        print(node.__class__.__name__)
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

class Visitor(NodeVisitor):

    def __init__(self):
        self.vars = {}

    def visit_Program(self, node):
        print("Running program", node.name)
        for vars_declaration_one in node.vars_declarations:
            self.visit(vars_declaration_one)
        self.visit(node.main)
        
    def visit_VarsDeclatrations(self, node):
        for var in node.vars:
            print("Var ", var.value, " of type ", node.vars_type)

    
    def visit_BinaryOperation(self, node):
        if node.type == Type.BinaryOperation.Plus:
            return self.visit(node.left) + self.visit(node.right)
        elif node.type == Type.BinaryOperation.Minus:
            return self.visit(node.left) - self.visit(node.right)
        elif node.type == Type.BinaryOperation.Mul:
            return self.visit(node.left) * self.visit(node.right)
        elif node.type == Type.BinaryOperation.Div:
            return self.visit(node.left) // self.visit(node.right)
        elif node.type == Type.BinaryOperation.Assign:
            self.vars[node.left.value] = self.visit(node.right)
            return self.vars[node.left.value]

    def visit_NoOperation(self, node):
        pass

    def visit_Compound(self, node):
        for i in node.children:
            self.visit(i)
        print(self.vars)
        
    def visit_Number(self, node):
        return node.value

    def visit_Var(self, node):
        return self.vars.get(node.value, 0)