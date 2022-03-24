MATH_RES= 1.0e-6

def EQ(r1: float, r2: float, res=MATH_RES) -> bool:
    return abs(r1-r2) <= res

def GT(r1: float, r2: float, res=MATH_RES) -> bool:
    return (r1 > r2 + res)

def LT(r1: float, r2: float, res=MATH_RES) -> bool:
    return (r1 < r2 - res)

def GE(r1: float, r2: float, res=MATH_RES) -> bool:
    return not LT(r1, r2, res)

def LE(r1: float, r2: float, res=MATH_RES) -> bool:
    return not GT(r1, r2, res)

def NE(r1: float, r2: float, res=MATH_RES) -> bool:
    return not EQ(r1, r2, res)

def ZERO(r: float, res=MATH_RES) -> bool:
    return abs(r) <= res

def POS(r: float, res=MATH_RES) -> bool:
    return (r > res)

def NEG(r: float, res=MATH_RES) -> bool:
    return (r < -res)