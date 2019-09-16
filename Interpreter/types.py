class Type:

    Word = 'Word'
    
    class Number:
        Integer = 'Integer'
        Float = 'Float'

    class BinaryOperation:
        Plus = 'Plus'
        Minus = 'Minus'
        Mul = 'Mul'
        Div = 'Div'
        Equal = 'Equal'
        Assign = 'Assign'

    class UnaryOperation:
        fill = 'fill'

    class Lang:
        Var = 'Var'
        LeftBracket = 'LeftBracket'
        RightBracket = 'RightBracket'
        Semi = 'Semi'
        Dot = 'Dot'
        Comma = 'Comma'
        Colon = 'Colon'

    class Reserved:
        Begin = 'BEGIN',
        End = 'END',
        Program = 'Program',
        Var = 'Var'

    class Special:
        EOF = 'EOF'