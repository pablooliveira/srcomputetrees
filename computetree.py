"""
computetree -- compute condition number and martingale length for any
               sum-product compute tree

computetree expects expression as a subset of FPCORE 2.0 s-expressions
    https://fpbench.org/spec/fpcore-2.0.html

Only trees with +, *, - binary operators are supported.

SymPy (https://www.sympy.org/) is required.
"""

from collections import namedtuple
import re
from sympy import Symbol, Abs, Integer, Float, simplify, factor, cancel

# Compile a regular expression to parse the s-expression delimiters
delimiters = '()*+- '
delimiters_re = re.compile('|'.join(['(\{})'.format(d) for d in delimiters]))

def tokenize(inp):
    """
        Tokenizes an s-expression returning a list of string tokens

        >>> tokenize('(+ (- u v) (* x y))')
        ['(', '+', '(', '-', 'u', 'v', ')', '(', '*', 'x', 'y', ')', ')']
    """
    def dropable(x): return x not in [None, ' ', '']
    return list(filter(dropable, re.split(delimiters_re, inp)))

def parse(inp):
    """
        Parses an s-expression as nested Python tuples
        >>> parse('(* (+ 3.14 a) (- x y))')
        ('*', ('+', 3.14, 'a'), ('-', 'x', 'y'))
    """
    def _parse_list(toks):
        while toks[0] != ')':
            yield _parse(toks)
        toks.pop(0)

    def _parse_tok(t):
        try:
            return float(t)
        except ValueError:
            return t

    def _parse(toks):
        t = toks.pop(0)
        return tuple(_parse_list(toks)) if t == '(' else _parse_tok(t)

    return _parse(tokenize(inp))

class Exp(namedtuple('Exp', ['v', 'm', 'K'])):
    """ Exp is the result of the evaluation of a computation tree.
        It is a named tuple with three fields:
            - m is the martingale length
            - v is the symbolic value
            - K is an upper-bound of the condition number
    """
    __slots__ = ()

    def __repr__(self):
        return 'm = {}\n'.format(self.m) + \
               'v = {}\n'.format(self.v) + \
               'K = {}'.format(self.K)



def evaluate(tree):
    """
    evaluates a parsed s-expression returning an Exp namedtuple
    K and m are evaluated recursively as shown in
        https://theses.hal.science/tel-04397409

    Computations are symbolic thanks to the SymPy library.
    """
    def _evaluate_v(v):
        return Exp(v=Symbol(v) if isinstance(v, str) else Float(v),
                   m=0,
                   K=Integer(1))

    def _evaluate_op(op, sx, sy):
        x = evaluate(sx)
        y = evaluate(sy)
        match op:
            case '*':
                return Exp(v=x.v * y.v,
                           m=x.m + y.m + 1,
                           K=x.K * y.K)
            case '+':
                return Exp(v=factor(x.v + y.v),
                           m=max(x.m, y.m) + 1,
                           K=factor(
                               Abs(x.v)/Abs(x.v + y.v) * x.K +
                               Abs(y.v)/Abs(x.v + y.v) * y.K))
            case '-':
                return Exp(v=factor(x.v - y.v),
                           m=max(x.m, y.m) + 1,
                           K=factor(
                               Abs(x.v)/Abs(x.v - y.v) * x.K +
                               Abs(y.v)/Abs(x.v - y.v) * y.K))

    match tree:
        case (op, x, y): return _evaluate_op(op, x, y)
        case v: return _evaluate_v(v)
