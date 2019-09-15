from Interpreter.token import Token
from Interpreter.Lexer.reserved_symbols import *
from Interpreter.types import Type

class Lexer():
    MAX_OPERATION_SIZE = 2

    def __init__(self, code: [str]):
        self.code = code
        self.current_code_part = code[0]
        self.current_code_line = 0
        self.code_lines = len(code)
        self.current_position = 0
        self.current_char = self.current_code_part[self.current_position]

    def advance(self):
        self.current_position += 1
        if self.current_position < len(self.current_code_part):
            self.current_char = self.current_code_part[self.current_position]
        else:
            self.current_code_line += 1
            if self.current_code_line < self.code_lines:
                self.current_code_part = self.code[self.current_code_line]
                self.current_position = 0
                self.current_char = self.current_code_part[0]
            else:
                self.current_char = None

    def lookup(self, count):
        peek_pos = self.current_position + count
        if peek_pos < len(self.current_code_part):
            return self.current_code_part[peek_pos]
        else:
            return None

    def skip_gaps(self):
        while self.current_char is not None and self.current_char == ' ':
            self.advance()

    def read_number(self):
        type = Type.Number.Integer
        result = ""
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        return Token(type, int(result))

    def read_word(self):
        type = Type.Word
        result = ""
        while self.current_char is not None and self.current_char.isalpha():
            result += self.current_char
            self.advance()

        if result in reserved_words:
            return Token(reserved_words[result], result)

        return Token(type, result)

    def read_operation(self):
        token = Token()
        operation = ""
        for i in range(self.MAX_OPERATION_SIZE):
            next_element = self.lookup(i)
            if next_element is None:
                break
            operation += next_element
            if operation in reserved_symbols.keys():
                token = Token(reserved_symbols[operation], operation)

        if token.value is not None:
            for i in range(len(operation)):
                self.advance()

        return token


    def next_token(self):
        self.skip_gaps()

        if self.current_char is None:
            return Token(Type.Special.EOF, None)
        elif self.current_char.isdigit():
            return self.read_number()
        elif self.current_char.isalpha():
            return self.read_word()
        else:
            return self.read_operation()
        