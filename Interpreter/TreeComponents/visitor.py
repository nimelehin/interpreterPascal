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

    def visit_UnaryOperation(self, node):
        if node.type == Type.BinaryOperation.Plus:
            return self.visit(node.left)
        elif node.type == Type.BinaryOperation.Minus:
            return -self.visit(node.left)
        
    def visit_Number(self, node):
        return node.value

    def visit_Var(self, node):
        return self.vars.get(node.value, 0)