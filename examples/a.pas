PROGRAM a;

procedure pr;
var a : INTEGER;
begin
    a := 300;
end;
end;

procedure sum(var a : INTEGER; b : INTEGER);
begin
    a := a + b;
end;
end;

function solve(a, b, c, x: INTEGER): Integer;
begin
    solve := a * x * x + b * x + c;
end;
end;

VAR
    a, b, c, x : INTEGER;
    flag : BOOLEAN;
BEGIN
    a := 1;
    b := 1;
    c := 1000;
    x := solve(a, 3, 4, 22) * -1;
    flag := (a = c) or (a = b);
    sum(x, c);
END.
