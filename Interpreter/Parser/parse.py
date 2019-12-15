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
        self.current_token_id = -1
        self.read_tokens = 0
        self.lexer_rich_the_end = 0
        self.tokens = []
        self.next_token()

    def next_token(self):
        self.current_token_id += 1
        self.token = self.get_token_at(self.current_token_id)
        print(self.token)

    def get_token_at(self, pos):
        if pos >= self.read_tokens and not self.lexer_rich_the_end:
            for i in range(pos - self.read_tokens + 1):
                self.tokens.append(self.lexer.next_token())
                self.read_tokens += 1
                if self.tokens[-1].type == Type.Special.EOF:
                    self.lexer_rich_the_end = True
                    break;

        return self.tokens[min(pos, self.read_tokens - 1)]

    def is_nth(self, type_of_token, n):
        if isinstance(type_of_token, list):
            for type_of_cur_token in type_of_token:
                if self.get_token_at(self.current_token_id+n).type == type_of_cur_token:
                    return True
            return False
        return self.get_token_at(self.current_token_id+n).type == type_of_token

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
        if self.is_next(Type.UnaryOperation.Plus) or self.is_next(Type.UnaryOperation.Minus):
            op_token = self.token
            self.next_token()
            result = Node.UnaryOperation(self.factor(), op_token)
            return result
        elif self.is_next(available_var_types):
            result = Node.Number(self.token)
            self.next_token()
            return result
        elif self.is_next(Type.Lang.LeftBracket):
            self.next_token()
            result = self.expr()
            self.must_next(Type.Lang.RightBracket)
            self.next_token()
            return result
        elif self.is_next(Type.Word) and self.is_nth(Type.Lang.LeftBracket, 1):
            return self.procedure_or_function_call()
        elif self.is_next(Type.Word):
            return self.variable()

    def term(self):
        print("HH", self.token)
        node = self.factor()
        while self.token.type in (Type.BinaryOperation.Mul, Type.BinaryOperation.Div, Type.BinaryOperation.Mod, Type.BinaryOperation.DivInt):
            operation_token = self.token
            self.next_token()
            new_node = self.factor()
            print("HH", self.token)
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

    def procedure_or_function_passed_params(self):
        if not self.is_next(Type.Lang.LeftBracket):
            return []
        self.next_token()
        if self.is_next(Type.Lang.RightBracket):
            return []

        params = [self.expr()]
        while self.token.type == Type.Lang.Comma:
            self.next_token()
            params.append(self.expr())

        self.must_next(Type.Lang.RightBracket)
        self.next_token()
        return params

    def procedure_or_function_call(self):
        print("FNC CALL")
        self.must_next(Type.Word)
        name_of_proc = self.token.value
        self.next_token()
        print("ok", name_of_proc)
        passed_params = self.procedure_or_function_passed_params()
        return Node.ProcedureOrFunctionCall(name_of_proc, passed_params);

    def statement(self):
        # assign_statement or compound_statement or empty
        if self.is_next(Type.Reserved.Begin):
            return self.compound_statement()

        if self.is_next(Type.Word) and self.is_nth(Type.BinaryOperation.Assign, 1):
            return self.assign_statement()

        if self.is_next(Type.Word) and (self.is_nth(Type.Lang.Semi, 1) or self.is_nth(Type.Lang.LeftBracket, 1)):
            print("here")
            return self.procedure_or_function_call()

        return Node.NoOperation()

    def statement_list(self):
        node = self.statement()
        result = [node]
        while self.token.type == Type.Lang.Semi:
            operation_token = self.token
            print("OP", operation_token)
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

    def vars_names(self):
        vars = [self.variable()]
        while self.token.type == Type.Lang.Comma:
            self.next_token()
            vars.append(self.variable())
        return vars

    def var_declarations(self):
        vars = self.vars_names()
        self.must_next(Type.Lang.Colon)
        self.next_token()
        cur_type = self.type_spec()
        self.must_next(Type.Lang.Semi)
        self.next_token()
        return Node.VarsDeclatrations(vars, cur_type)

    def declarations(self):
        if not self.is_next(Type.Reserved.Var):
            return []

        self.must_next(Type.Reserved.Var)
        self.next_token()
        result = [self.var_declarations()]
        while self.token.type != Type.Reserved.Begin:
            result.append(self.var_declarations())
        return result

    def procedure_params_vars(self):
        referenced = False

        # check if params are passed by reference
        if self.is_next(Type.Reserved.Var):
            referenced = True
            self.next_token()

        vars = [self.variable()]
        while self.token.type == Type.Lang.Comma:
            self.next_token()
            vars.append(self.variable())
        self.must_next(Type.Lang.Colon)
        self.next_token()
        cur_type = self.type_spec()
        return Node.ProcedureOrFunctionVarsDeclatrations(vars, cur_type, referenced)

    def procedure_or_function_params(self):
        result = []
        if not self.is_next(Type.Lang.LeftBracket):
            return result

        self.next_token()

        if (self.is_next([Type.Word, Type.Reserved.Var])):
            result.append(self.procedure_params_vars())
            while self.token.type == Type.Lang.Semi:
                self.next_token()
                result.append(self.procedure_params_vars())

        self.must_next(Type.Lang.RightBracket)
        self.next_token()
        return result

    def procedure_definition(self):
        # eating procedure keyword
        self.must_next(Type.Reserved.Procedure)
        self.next_token()

        # eating name of procedure
        self.must_next(Type.Word)
        procedure_name = self.token.value
        self.next_token()

        #eating procedure params if have
        procedure_params = self.procedure_or_function_params()

        # eating ;
        self.must_next(Type.Lang.Semi)
        self.next_token()

        vars_declarations = self.declarations()
        main_function = self.compound_statement()
        self.must_next(Type.Lang.Semi)
        self.next_token()
        self.must_next(Type.Reserved.End)
        self.next_token()
        self.must_next(Type.Lang.Semi)
        self.next_token()

        return Node.Procedure(procedure_name, procedure_params, vars_declarations, main_function)

    def function_definition(self):
        # eating procedure keyword
        self.must_next(Type.Reserved.Function)
        self.next_token()

        # eating name of procedure
        self.must_next(Type.Word)
        function_name = self.token.value
        self.next_token()

        # eating procedure params if have
        function_params = self.procedure_or_function_params()

        # eating return type
        self.must_next(Type.Lang.Colon)
        self.next_token()
        function_return_type = self.type_spec()

        # eating ;
        self.must_next(Type.Lang.Semi)
        self.next_token()

        vars_declarations = self.declarations()
        main_function = self.compound_statement()
        self.must_next(Type.Lang.Semi)
        self.next_token()
        self.must_next(Type.Reserved.End)
        self.next_token()
        self.must_next(Type.Lang.Semi)
        self.next_token()

        return Node.Function(function_name, function_params, function_return_type, vars_declarations, main_function)


    def procedures_and_functions(self):
        res = []
        print(self.token)
        while self.is_next([Type.Reserved.Procedure, Type.Reserved.Function]):
            if (self.is_next(Type.Reserved.Procedure)):
                res.append(self.procedure_definition())

            if (self.is_next(Type.Reserved.Function)):
                res.append(self.function_definition())

        return res

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
        procedures = self.procedures_and_functions()
        vars_declarations = self.declarations()
        main_function = self.compound_statement()
        self.must_next(Type.Lang.Dot)
        return Node.Program(program_name, procedures, vars_declarations, main_function)
