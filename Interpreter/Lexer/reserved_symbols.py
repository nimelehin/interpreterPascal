from Interpreter.types import Type

reserved_symbols = {
    '+': Type.BinaryOperation.Plus,
    '-': Type.BinaryOperation.Minus,
    '*': Type.BinaryOperation.Mul,
    '/': Type.BinaryOperation.Div,
    '(': Type.Lang.LeftBracket,
    ')': Type.Lang.RightBracket,
    ';': Type.Lang.Semi,
    '.': Type.Lang.Dot,
    ':=': Type.BinaryOperation.Assign,
    ',': Type.Lang.Comma,
    ':': Type.Lang.Colon,

    '=': Type.BinaryOperation.Equal,
    '<>': Type.BinaryOperation.NotEqual,
    '<': Type.BinaryOperation.Less,
    '<=': Type.BinaryOperation.LessEqual,
    '>': Type.BinaryOperation.Bigger,
    '>=': Type.BinaryOperation.BiggerEqual,
}

reserved_words = {
    'BEGIN': Type.Reserved.Begin,
    'END': Type.Reserved.End,
    'DIV': Type.BinaryOperation.DivInt,
    'AND': Type.BinaryOperation.And,
    'OR': Type.BinaryOperation.Or,
    'NOT': Type.UnaryOperation.Not,
    'PROGRAM': Type.Reserved.Program,
    'PROCEDURE': Type.Reserved.Procedure,
    'FUNCTION': Type.Reserved.Function,
    'VAR': Type.Reserved.Var,
    'TRUE': Type.Number.Boolean,
    'FALSE': Type.Number.Boolean,
}

reserved_words_present_as = {
    'TRUE': True,
    'FALSE': False,
}

available_var_types = [Type.Number.Integer, Type.Number.Real, Type.Number.Boolean]
