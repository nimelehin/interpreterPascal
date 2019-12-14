from Interpreter.types import Type

class NodeVisitor():
    def visit(self, node):
        print(node.__class__.__name__)
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def choose_type(self, left, right, must=None):
        if must is None:
            if left == Type.Number.Real or right == Type.Number.Real:
                return Type.Number.Real
            else:
                return Type.Number.Integer
        else:
            if must == left == right:
                return must
            else:
                print("Diff types: ", left, right, must)
                exit(0)

class Visitor(NodeVisitor):

    def __init__(self):
        self.procedures = {}
        self.vars = {}
        self.var_types = {}

    def visit_Program(self, node):
        print("Running program", node.name)
        for procedure in node.procedures:
            self.procedures[procedure.name] = procedure
        for vars_declaration_one in node.vars_declarations:
            self.visit(vars_declaration_one)
        self.visit(node.main)
        print(self.vars)

    def visit_Procedure(self, node):
        last_vars = self.vars
        last_var_types = self.var_types

        self.vars = {}
        self.var_types = {}

        for vars_declaration_one in node.vars_declarations:
            self.visit(vars_declaration_one)
        self.visit(node.main)

        print(self.vars)

        self.vars = last_vars
        self.var_types = last_var_types


    def visit_ProcedureCall(self, node):
        if (self.procedures.get(node.name, None) == None):
            print("[Err] No such proc")
            exit(1)
        self.visit(self.procedures[node.name])

    def visit_VarsDeclatrations(self, node):
        for var in node.vars:
            print("Var ", var.value, " of type ", node.vars_type)
            self.var_types[var.value] = node.vars_type
            if node.vars_type == Type.Number.Integer:
                self.vars[var.value] = 0
            else:
                self.vars[var.value] = 0.0

    def visit_BinaryOperation(self, node):
        if node.type == Type.BinaryOperation.Plus:
            lop, ltype = self.visit(node.left)
            rop, rtype = self.visit(node.right)
            return (lop + rop, self.choose_type(ltype, rtype))
        elif node.type == Type.BinaryOperation.Minus:
            lop, ltype = self.visit(node.left)
            rop, rtype = self.visit(node.right)
            return (lop - rop, self.choose_type(ltype, rtype))
        elif node.type == Type.BinaryOperation.Mul:
            lop, ltype = self.visit(node.left)
            rop, rtype = self.visit(node.right)
            return (lop * rop, self.choose_type(ltype, rtype))
        elif node.type == Type.BinaryOperation.Div:
            lop, ltype = self.visit(node.left)
            rop, rtype = self.visit(node.right)
            return (lop / rop, Type.Number.Real)
        elif node.type == Type.BinaryOperation.DivInt:
            lop, ltype = self.visit(node.left)
            rop, rtype = self.visit(node.right)
            return (lop // rop, self.choose_type(ltype, rtype, Type.Number.Integer))

    def visit_AssignOperation(self, node):
        op, type = self.visit(node.expr)
        if self.var_types[node.var_id] == Type.Number.Integer:
            self.vars[node.var_id] = op
        else:
            self.vars[node.var_id] = op
        return (self.vars[node.var_id], self.var_types[node.var_id])

    def visit_NoOperation(self, node):
        pass

    def visit_Compound(self, node):
        for i in node.children:
            self.visit(i)
        # print(self.vars)

    def visit_Number(self, node):
        return (node.value, node.type)

    def visit_Var(self, node):
        return (self.vars[node.value], self.var_types[node.value])
