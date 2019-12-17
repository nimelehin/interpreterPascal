PROGRAM branches;

function solve(a: INTEGER; var steps: INTEGER): Integer;
begin
    if a = 0 then begin
        steps := 1;
        solve := 1
    end else begin
        solve := 2 * solve(a-1, steps);
        steps := steps + 1;
    end;
end;
end;

VAR
    ai, bi, ci: INTEGER;
BEGIN

    ai := 5;
    bi := solve(ai, ci);
END.
