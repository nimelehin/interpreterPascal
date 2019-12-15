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

    class AssignOperation(Basic):
        def __init__(self, var_id, expr):
            self.var_id = var_id
            self.expr = expr
            self.type = 'AssignOperation'

    class VarsDeclatrations(Basic):
        def __init__(self, vars, vars_type):
            self.vars = vars
            self.vars_type = vars_type
            self.type = 'VarsDeclatrations'

    class ProcedureOrFunctionVarsDeclatrations(Basic):
        def __init__(self, vars, vars_type, referenced):
            self.vars = vars
            self.vars_type = vars_type
            self.referenced = referenced
            self.type = 'ProcedureOrFunctionVarsDeclatrations'

    class ProcedureOrFunctionCall(Basic):
        def __init__(self, name, passed_params):
            self.name = name
            self.passed_params = passed_params
            self.type = 'ProcedureCall'

    class Procedure(Basic):
        def __init__(self, name, params, vars_declarations, main):
            self.name = name
            self.params = params
            self.vars_declarations = vars_declarations
            self.main = main
            self.type = 'Procedure'

    class Function(Procedure):
        def __init__(self, name, params, ret_type, vars_declarations, main):
            super().__init__(name, params, vars_declarations, main)
            self.return_type = ret_type
            self.type = 'Function'

    class Program(Basic):
        def __init__(self, name, procedures, vars_declarations, main):
            self.name = name
            self.procedures = procedures
            self.vars_declarations = vars_declarations
            self.main = main
            self.type = 'Program'
