from Interpreter.types import Type

reserved_symbols = {
    '+': Type.BinaryOperation.Plus,
    '-': Type.BinaryOperation.Minus,
    '=': Type.BinaryOperation.Equal,
    '*': Type.BinaryOperation.Mul,
    '/': Type.BinaryOperation.Div,
    '(': Type.Lang.LeftBracket,
    ')': Type.Lang.RightBracket,
    ';': Type.Lang.Semi,
    '.': Type.Lang.Dot,
    ':=': Type.BinaryOperation.Assign,
    ',': Type.Lang.Comma,
    ':': Type.Lang.Colon,
}

reserved_words = {
    'BEGIN': Type.Reserved.Begin,
    'END': Type.Reserved.End,
    'DIV': Type.BinaryOperation.DivInt,
    'PROGRAM': Type.Reserved.Program,
    'PROCEDURE': Type.Reserved.Procedure,
    'FUNCTION': Type.Reserved.Function,
    'VAR': Type.Reserved.Var,
}

available_var_types = [Type.Number.Integer, Type.Number.Real]
