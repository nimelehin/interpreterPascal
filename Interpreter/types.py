class Type:

    Word = 'WORD'

    class Number:
        Integer = 'INTEGER'
        Real = 'REAL'
        Boolean = 'BOOLEAN'

    class BinaryOperation:
        Plus = 'PLUS'
        Minus = 'MINUS'
        Mul = 'MUL'
        Div = 'DIV'
        DivInt = 'DIVINT'
        Mod = 'MOD'

        Assign = 'ASSIGN'

        And = 'AND'
        Or = 'OR'
        Equal = 'EQUAL'
        NotEqual = "NOTEQUAL"
        Less = "LESS"
        LessEqual = "LESSEQUAL"
        Bigger = "BIGGER"
        BiggerEqual = "BIGGEREQUAL"

    class UnaryOperation:
        fill = 'FILL'
        Plus = 'PLUS'
        Minus = 'MINUS'
        Not = 'NOT'

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
        Procedure = 'PROCEDURE'
        Function = 'FUNCTION'

    class Special:
        EOF = 'EOF'
