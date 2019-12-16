from Interpreter.types import Type

class NodeVisitor():
    def visit(self, node, params=None):
        print(node.__class__.__name__)
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node, params)

    def generic_visit(self, node, params=None):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def check_type(self, tp, must):
        if must == tp:
            return must
        else:
            print("Diff types: ", left, right, must)
            exit(0)

    def cast_type(self, left, right, must=None):
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

    def visit_Program(self, node, params=None):
        print("Running program", node.name)
        for procedure in node.procedures:
            self.procedures[procedure.name] = procedure
        for vars_declaration_one in node.vars_declarations:
            self.visit(vars_declaration_one)
        self.visit(node.main)
        print(self.vars)

    def visit_Procedure(self, node, params):
        last_vars = self.vars
        last_var_types = self.var_types
        self.vars = {}
        self.var_types = {}
        reference_table = {}
        now = 0

        # setting params for procedure
        for parametr in node.params:
            for var in parametr.vars:
                passed_var_name, passed_value = params[now]
                passed_value, passed_type_of_value = passed_value

                self.vars[var.value] = passed_value
                self.var_types[var.value] = parametr.vars_type
                if parametr.referenced:
                    reference_table[var.value] = passed_var_name
                now += 1

        # vars declaration
        for vars_declaration_one in node.vars_declarations:
            self.visit(vars_declaration_one)
        self.visit(node.main)

        for updwithvar, updvar in reference_table.items():
            last_vars[updvar] = self.vars[updwithvar]
        self.vars = last_vars
        self.var_types = last_var_types

    def visit_Function(self, node, params):
        last_vars = self.vars
        last_var_types = self.var_types
        self.vars = {}
        self.var_types = {}
        reference_table = {}
        now = 0
        self.vars[node.name] = 0
        self.var_types[node.name] = node.return_type

        # setting params for procedure
        for parameter in node.params:
            for var in parameter.vars:
                passed_var_name, passed_value = params[now]
                passed_value, passed_type_of_value = passed_value

                self.vars[var.value] = passed_value
                self.var_types[var.value] = parameter.vars_type
                if parameter.referenced:
                    reference_table[var.value] = passed_var_name
                now += 1

        # vars declaration
        for vars_declaration_one in node.vars_declarations:
            print(vars_declaration_one)
            self.visit(vars_declaration_one)
        self.visit(node.main)

        result = (self.vars[node.name], self.var_types[node.name])
        for updwithvar, updvar in reference_table.items():
            last_vars[updvar] = self.vars[updwithvar]
        self.vars = last_vars
        self.var_types = last_var_types
        print("Function answer ", result)
        return result

    def visit_ProcedureOrFunctionCall(self, node, params=None):
        if (self.procedures.get(node.name, None) == None):
            print("[Err] No such proc")
            exit(1)

        values = []

        for param_node in node.passed_params:
            value = self.visit(param_node)
            result = (None, value)
            # means that var
            if param_node.type == 'WORD' or param_node.type == 'VAR':
                # saving param name (used for refernce values)
                result = (param_node.value, value)
            values.append(result)

        return self.visit(self.procedures[node.name], values)

    def visit_VarsDeclatrations(self, node, params=None):
        for var in node.vars:
            print("Var ", var.value, " of type ", node.vars_type)
            self.var_types[var.value] = node.vars_type
            if node.vars_type == Type.Number.Integer:
                self.vars[var.value] = 0
            elif node.vars_type == Type.Number.Real:
                self.vars[var.value] = 0.0
            elif node.vars_type == Type.Number.Boolean:
                self.vars[var.value] = False
            else:
                print("Unsupported type")
                exit(0)

    def visit_BinaryOperation(self, node, params=None):
        lop, ltype = self.visit(node.left)
        rop, rtype = self.visit(node.right)

        if node.type == Type.BinaryOperation.Plus:
            return (lop + rop, self.cast_type(ltype, rtype))
        elif node.type == Type.BinaryOperation.Minus:
            return (lop - rop, self.cast_type(ltype, rtype))
        elif node.type == Type.BinaryOperation.Mul:
            return (lop * rop, self.cast_type(ltype, rtype))
        elif node.type == Type.BinaryOperation.Div:
            return (lop / rop, Type.Number.Real)
        elif node.type == Type.BinaryOperation.DivInt:
            return (lop // rop, self.cast_type(ltype, rtype, Type.Number.Integer))
        

        # boolean operations
        elif node.type == Type.BinaryOperation.And:
            return (lop and rop, Type.Number.Boolean)
        elif node.type == Type.BinaryOperation.Or:
            return (lop or rop, Type.Number.Boolean)

        elif node.type == Type.BinaryOperation.Equal:
            return (lop == rop, Type.Number.Boolean)
        elif node.type == Type.BinaryOperation.NotEqual:
            return (lop != rop, Type.Number.Boolean)
        elif node.type == Type.BinaryOperation.Less:
            return (lop < rop, Type.Number.Boolean)
        elif node.type == Type.BinaryOperation.LessEqual:
            return (lop <= rop, Type.Number.Boolean)
        elif node.type == Type.BinaryOperation.Bigger:
            return (lop > rop, Type.Number.Boolean)
        elif node.type == Type.BinaryOperation.BiggerEqual:
            return (lop >= rop, Type.Number.Boolean)

    def visit_UnaryOperation(self, node, params=None):
        lop, ltype = self.visit(node.left)
        if node.type == Type.UnaryOperation.Plus:
            return (lop, ltype)
        elif node.type == Type.UnaryOperation.Minus:
            return (-lop, ltype)
        elif node.type == Type.UnaryOperation.Not:
            return (not lop, self.check_type(ltype, Type.Number.Boolean))

    def visit_AssignOperation(self, node, params=None):
        op, type = self.visit(node.expr)
        self.vars[node.var_id] = op
        return (self.vars[node.var_id], self.var_types[node.var_id])

    def visit_NoOperation(self, node, params=None):
        pass

    def visit_Compound(self, node, params=None):
        for i in node.children:
            self.visit(i)
        # print(self.vars)

    def visit_Number(self, node, params=None):
        return (node.value, node.type)

    def visit_Var(self, node, params=None):
        return (self.vars[node.value], self.var_types[node.value])
