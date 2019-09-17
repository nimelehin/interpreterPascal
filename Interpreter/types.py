class Type:

    Word = 'WORD'
    
    class Number:
        Integer = 'INTEGER'
        Real = 'REAL'

    class BinaryOperation:
        Plus = 'PLUS'
        Minus = 'MINUS'
        Mul = 'MUL'
        Div = 'DIV'
        DivInt = 'DIVINT'
        Mod = 'MOD'
        Equal = 'EQUAL'
        Assign = 'ASSIGN'

    class UnaryOperation:
        fill = 'FILL'

    class Lang:
        Var = 'VAR'
        LeftBracket = 'LeftBracket'
        RightBracket = 'RightBracket'
        Semi = 'SEMI'
        Dot = 'DOT'
        Comma = 'COMMA'
        Colon = 'COLON'

    class Reserved:
        Begin = 'BEGIN'
        End = 'END'
        Program = 'PROGRAM'
        Var = 'VAR'

    class Special:
        EOF = 'EOF'