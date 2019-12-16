PROGRAM a;

VAR
    ai, bi, ci : INTEGER;
    ar, br, cr : REAL;
    a, b, c, d, e, f, x, y, z : BOOLEAN;
BEGIN

    ai := (1 + 2) div 333 + 1;
    bi := 2;
    ci := 40 and 33 and 1;
    ar := 2.3 * 5.6;

    a := ai + bi + ai = ci div 10;
    b := (not a and not b) or (ai * 2 + ci - 38 > 200 + ai);
    c := ai + bi + ai < ci;
    d := (1 <> 1);
    e := 1 >= 1;
    f := (1 + 2 >= 3) or false or (1 > 0);

    x := (ar > 19);
    y := (ar > 19) and ((ai + bi) div 2 > 0);
    z := (1 > 0) and (2 > 0);
END.
