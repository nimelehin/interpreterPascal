from Interpreter.Lexer.lexer import Lexer
from Interpreter.types import Type
from Interpreter.token import Token
from Interpreter.TreeComponents.nodes import Node
from Interpreter.Lexer.reserved_symbols import available_var_types

class Parser():

    def __init__(self):
        pass
        

    def set_code_lines(self, code: [str]):
        self.lexer = Lexer(code)
        self.token = Token()
        self.tokens = []
        self.next_token()

    def next_token(self):
        self.token = self.lexer.next_token()
        print(self.token)
        self.tokens.append(self.token)

    def is_next(self, type_of_token):
        if isinstance(type_of_token, list):
            for type_of_cur_token in type_of_token:
                if self.token.type == type_of_cur_token:
                    return True
            return False
        return self.token.type == type_of_token

    def must_next(self, type_of_token):
        if not self.is_next(type_of_token):
            print("{0} is not {1}".format(self.token, type_of_token))
            exit(1)
        
    def variable(self):
        self.must_next(Type.Word)
        result = Node.Var(self.token)
        self.next_token()
        return result

    def factor(self):
        result = None
        if self.is_next(Type.BinaryOperation.Plus) or self.is_next(Type.BinaryOperation.Minus):
            op_token = self.token
            self.next_token()
            result = Node.UnaryOperation(self.factor(), op_token)
        elif self.is_next(available_var_types):
            result = Node.Number(self.token)
        elif self.is_next(Type.Lang.LeftBracket):
            self.next_token()
            result = self.expr()
            self.must_next(Type.Lang.RightBracket)
        elif self.is_next(Type.Word):
            return self.variable()
        self.next_token()
        return result
        
    def term(self):
        node = self.factor()
        while self.token.type in (Type.BinaryOperation.Mul, Type.BinaryOperation.Div, Type.BinaryOperation.Mod, Type.BinaryOperation.DivInt):
            operation_token = self.token
            self.next_token()
            new_node = self.factor()
            node = Node.BinaryOperation(node, new_node, operation_token)
        return node

    def expr(self):
        node = self.term()
        while self.token.type in (Type.BinaryOperation.Plus, Type.BinaryOperation.Minus):
            operation_token = self.token
            self.next_token()
            new_node = self.term()
            node = Node.BinaryOperation(node, new_node, operation_token)
        return node

    def assign_statement(self):
        node = self.variable()
        while self.token.type == Type.BinaryOperation.Assign:
            operation_token = self.token
            self.next_token()
            new_node = self.expr()
            node = Node.AssignOperation(node.value, new_node)
        return node

    def statement(self):
        # assign_statement or compound_statement or empty
        if self.is_next(Type.Reserved.Begin):
            return self.compound_statement()

        if self.is_next(Type.Word):
            return self.assign_statement()

        return Node.NoOperation()

    def statement_list(self):
        node = self.statement()
        result = [node]
        while self.token.type == Type.Lang.Semi:
            operation_token = self.token
            self.next_token()
            node = self.statement()
            result.append(node)
        return result

    def compound_statement(self):
        self.must_next(Type.Reserved.Begin)
        self.next_token()
        node = Node.Compound(self.statement_list())
        self.must_next(Type.Reserved.End)
        self.next_token()
        return node

    def type_spec(self):
        self.must_next(Type.Word)
        vars_type = None
        if self.token.value.upper() in available_var_types:
            vars_type = self.token.value.upper()
        self.next_token()
        return vars_type

    def var_declarations(self):
        vars = [self.variable()]
        while self.token.type == Type.Lang.Comma:
            self.next_token()
            vars.append(self.variable())
        self.must_next(Type.Lang.Colon)
        self.next_token()
        cur_type = self.type_spec()
        self.must_next(Type.Lang.Semi)
        self.next_token()
        return Node.VarsDeclatrations(vars, cur_type)

    def declarations(self):
        if not self.is_next(Type.Reserved.Var):
            return

        self.must_next(Type.Reserved.Var)
        self.next_token()
        result = [self.var_declarations()]
        while self.token.type != Type.Reserved.Begin:
            result.append(self.var_declarations())
        return result

    def program_init(self):
        self.must_next(Type.Reserved.Program)
        self.next_token()
        self.must_next(Type.Word)
        name = self.token.value
        self.next_token()
        self.must_next(Type.Lang.Semi)
        self.next_token()
        return name

    def program(self):
        program_name = self.program_init()
        vars_declarations = self.declarations()
        main_function = self.compound_statement()
        self.must_next(Type.Lang.Dot)
        return Node.Program(program_name, vars_declarations, main_function)