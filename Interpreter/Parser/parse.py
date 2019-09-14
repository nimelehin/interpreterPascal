from Interpreter.Lexer.lexer import Lexer
from Interpreter.types import Type
from Interpreter.token import Token
from Interpreter.TreeComponents.nodes import Node

class Parser():

    def __init__(self):
        pass
        

    def set_code_line(self, code):
        self.lexer = Lexer(code)
        self.token = Token()
        self.tokens = []
        self.next_token()

    def next_token(self):
        self.token = self.lexer.next_token()
        self.tokens.append(self.token)

    def is_next(self, type_of_token):
        return self.token.type == type_of_token

    def must_next(self, type_of_token):
        if not self.is_next(type_of_token):
            print("{0} is not {1}".format(self.token, type_of_token))
            exit(1)
        
    def factor(self):
        result = None
        if self.is_next(Type.BinaryOperation.Plus) or self.is_next(Type.BinaryOperation.Minus):
            op_token = self.token
            self.next_token()
            result = Node.UnaryOperation(self.factor(), op_token)
        elif self.is_next(Type.Number.Integer):
            result = Node.Number(self.token)
        elif self.is_next(Type.Lang.LeftBracket):
            self.next_token()
            result = self.expr()
            self.must_next(Type.Lang.RightBracket)
        elif self.is_next(Type.Word):
            result = Node.Var(self.token)
        self.next_token()
        return result
        
    def term(self):
        node = self.factor()
        while self.token.type in (Type.BinaryOperation.Mul, Type.BinaryOperation.Div):
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

    def assign(self):
        node = self.factor()
        while self.token.type in (Type.BinaryOperation.Assign):
            operation_token = self.token
            self.next_token()
            new_node = self.expr()
            node = Node.BinaryOperation(node, new_node, operation_token)
        return node

    def statement(self):
        # assign_statement or compound_statement or empty
        if self.is_next(Type.Reserved.Begin):
            return self.compound_statement()

        if self.is_next(Type.Word):
            return self.assign()

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

    def program(self):
        result = self.compound_statement()
        self.must_next(Type.Lang.Dot)
        return result