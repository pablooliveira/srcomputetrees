""" Compute Karatsuba martingale lenghts
"""

from computetree import evaluate

def padd(A,B):
    assert len(A) == len(B)
    def _add(a,b):
        match a,b:
            case a,0: return a
            case 0,b: return b
            case a,b: return ('+', a, b)
    return [_add(a,b) for a,b in zip(A,B)]

def psub(A,B):
    assert len(A) == len(B)
    def _sub(a,b):
        match a,b:
            case a,0: return a
            case a,b: return ('-', a, b)
    return [_sub(a,b) for a,b in zip(A,B)]

def shift(A, n):
    return [0] * n + A

def complete(A, n):
    return A + [0] * (n - len(A))

def karatsuba(A,B):
    n = len(A)
    assert n == len(B)
    if n == 1: return [('*', A[0], B[0])]
    h = n//2
    Al, Au = A[:h], A[h:]
    Bl, Bu = B[:h], B[h:]
    D0 = karatsuba(Al, Bl)
    D1 = karatsuba(Au, Bu)
    D2 = karatsuba(padd(Al,Au), padd(Bl, Bu))

    return padd(
            complete(shift(D2, h), 2*n),
            padd(
                psub(
                    complete(shift(D1, n), 2*n),
                    complete(shift(D1, h), 2*n)),
                psub(
                    complete(D0, 2*n),
                    complete(shift(D0, h), 2*n))))


def naive(A,B):
    assert len(A) == len(B)
    n = len(A)
    if n == 1:
        return [('*', A[0], B[0])]
    h = n//2
    Al, Au = A[:h], A[h:]
    Bl, Bu = B[:h], B[h:]
    D0 = naive(Al, Bl)
    D1 = naive(Au, Bu)
    D2 = padd(naive(Al,Bu), naive(Au, Bl))

    return padd(padd(complete(D0, 2*n),
                     complete(shift(D1, n), 2*n)),
                 complete(shift(D2, h), 2*n))

for k in range(2,8):
    N = 2**k
    K = karatsuba(
            ['a{}'.format(d) for d in range(N)],
            ['b{}'.format(d) for d in range(N)])

    m = max([evaluate(K[i], symbolic=False).m for i in range(N*2)])
    print("m({}) = {}".format(N, m))
