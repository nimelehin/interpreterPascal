from Interpreter.token import Token
from Interpreter.Lexer.reserved_symbols import *
from Interpreter.types import Type

class Lexer():
    def __init__(self, code):
        self.code = code
        self.current_position = 0
        self.current_char = self.code[self.current_position]

    def advance(self):
        self.current_position += 1
        if self.current_position < len(self.code):
            self.current_char = self.code[self.current_position]
        else:
            self.current_char = None

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

        return Token(type, result)

    def get_next_token(self):
        self.skip_gaps()

        if self.current_char is None:
            return Token(Type.Special.EOF, None)
        elif self.current_char.isdigit():
            return self.read_number()
        elif self.current_char.isalpha():
            return self.read_word()
        elif self.current_char in reserved_symbols.keys():
            token = Token(reserved_symbols[self.current_char], self.current_char)
            self.advance()
            return token
        