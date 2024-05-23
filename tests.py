"""
>>> recursive = parse('(+ (+ (+ a1 a2) a3) a4)')
>>> evaluate(recursive)
m = 3
v = a1 + a2 + a3 + a4
K = (Abs(a1) + Abs(a2) + Abs(a3) + Abs(a4))/Abs(a1 + a2 + a3 + a4)

>>> pairwise = parse('(+ (+ a1 a2) (+ a3 a4))')
>>> evaluate(pairwise)
m = 2
v = a1 + a2 + a3 + a4
K = (Abs(a1) + Abs(a2) + Abs(a3) + Abs(a4))/Abs(a1 + a2 + a3 + a4)

>>> poly = parse('(+ a0 (+ (* a1 x) (+ (* (* a2 x) x) (* (* (* a3 x) x) x))))')
>>> evaluate(poly)
m = 6
v = a0 + a1*x + a2*x**2 + a3*x**3
K = (Abs(a0) + Abs(a1*x) + Abs(a2*x**2) + Abs(a3*x**3))/Abs(a0 + a1*x + a2*x**2 + a3*x**3)

>>> horner = parse('(+ (* (+ (* (+ (* a3 x) a2) x) a1) x) a0)')
>>> evaluate(horner)
m = 6
v = a0 + a1*x + a2*x**2 + a3*x**3
K = (Abs(a0)*Abs(a2 + a3*x)*Abs(a1 + a2*x + a3*x**2) + Abs(a1)*Abs(a2 + a3*x)*Abs(a1*x + a2*x**2 + a3*x**3) + Abs(a2)*Abs(a2*x + a3*x**2)*Abs(a1*x + a2*x**2 + a3*x**3) + Abs(a3*x)*Abs(a2*x + a3*x**2)*Abs(a1*x + a2*x**2 + a3*x**3))/(Abs(a2 + a3*x)*Abs(a1 + a2*x + a3*x**2)*Abs(a0 + a1*x + a2*x**2 + a3*x**3))

>>> factored1 = parse('(* (+ x 8) (* (+ x 5) (* (+ x 3) (- x 2))))')
>>> E1 = evaluate(factored1)
>>> E1.v.subs('x', 1.0)
-216.000000000000
>>> E1.m
7
>>> E1.K.subs('x', 1.0)
3.00000000000000
>>> E1.K.subs('x', -2.999)
52742.8772115700

>>> naive2 = parse('(- (- (+ (+ (* (* (* x x) x) x) (* (* (* 14 x) x) x)) (* (* 47 x) x)) (* 38 x)) 240))')
>>> E2 = evaluate(naive2)
>>> E2.v.subs('x', 1.0)
-216.000000000000
>>> E2.m
7
>>> E2.K.subs('x', 1.0)
1.57407407407407
>>> E2.K.subs('x', -2.999)
24691.5397577340

>>> horner3 = parse('(- (* (- (* (+ (* (+ x 14 ) x) 47) x) 38) x) 240)')
>>> E3 = evaluate(horner3)
>>> E3.v.subs('x', 1.0)
-216.000000000000
>>> E3.m
7
>>> E3.K.subs('x', 1.0)
1.57407407407407
>>> E3.K.subs('x', -2.999)
24691.5397577340

>>> pairwise4 = parse('(- (+ (+ (* (* (* x x) x) x) (* (* (* 14 x) x) x)) (- (* (* 47 x) x) (* 38 x))) 240)')
>>> E4 = evaluate(pairwise4)
>>> E4.v.subs('x', 1.0)
-216.000000000000
>>> E4.m
6
>>> E4.K.subs('x', 1.0)
1.57407407407407
>>> E4.K.subs('x', -2.999)
24691.5397577340


>>> tcheb1 = parse('(- (+ (- (+ (- (* (* (* (* (* (* (* (* (* (* (* 1024 x) x) x) x) x) x) x) x) x) x) x) (* (* (* (* (* (* (* (* (* 2816 x) x) x) x) x) x) x) x) x)) (* (* (* (* (* (* (* 2816 x) x) x) x) x) x) x)) (* (* (* (* (* 1232 x) x) x) x) x)) (* (* (* 220 x) x) x)) (* 11 x))')
>>> E5 = evaluate(tcheb1)
>>> E5.m
16
>>> E5.K.subs('x', .5)
199.000000000000
>>> E5.K.subs('x', .999)
9140.08093288036
"""

from computetree import evaluate, parse
