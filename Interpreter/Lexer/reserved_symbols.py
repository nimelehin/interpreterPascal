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
}
