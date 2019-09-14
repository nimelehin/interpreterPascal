BEGIN
    a = 1;
    b = 3;
    c = 2 * b + a;
    BEGIN
        anotherA = a - 2;
        anotherV = a + 2;
        anotherC = c * 10 + anotherA;
    END;
END.