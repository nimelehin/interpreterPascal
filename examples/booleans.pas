PROGRAM a;

VAR
    ai, bi, ci : INTEGER;
    a, b, c, d, e, f : BOOLEAN;
BEGIN
    
    ai := 1;
    bi := 2;
    ci := 40;

    a := (ai + bi + ai) = (ci div 10);
    b := not a;
    c := (ai + bi + ai) < (ci);
    d := (1 <> 1);
    e := (1 >= 1);
    f := (a and e) and (c or d);
END.
