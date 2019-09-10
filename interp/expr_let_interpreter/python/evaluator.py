from expr import Op

from collections import defaultdict

# ad-hoc environments

# the environemt is a dictionary of stacks
class Environment:
    def __init__(self):
        self._env = defaultdict(list)

    def lookup(self, var):
        return self._env[var][-1]

    def extend(self, var, value):
        self._env[var].append(value)

    def pop(self, var):
        self._env[var].pop()

class EvaluateVisitor:
    env = None

    @staticmethod
    def literal(n):
        return n
    
    @staticmethod
    def variable(v):
        try:
            return EvaluateVisitor.env.lookup(v)
        except IndexError:
            raise Exception(f"Variable not bound: {v}")

    @staticmethod
    def binary(e1, op, e2):
        v1 = evaluate_iter(e1)
        v2 = evaluate_iter(e2)
        if op == Op.Plus:
            return v1 + v2
        elif op == Op.Mult:
            return v1 * v2
    
    @staticmethod
    def let(var, e1, e2):
        v1 = evaluate_iter(e1)
        EvaluateVisitor.env.extend(var, v1)
        # evaluate e2 in the extended environment
        v2 = evaluate_iter(e2)
        # restore the previous environment
        EvaluateVisitor.env.pop(var)
        return v2

def evaluate_iter(expr):
    return expr.accept_visitor(EvaluateVisitor)

def evaluate(expr):
    # TODO: representing env as a global variable
    # is not very elegant, but this way we don't have
    # to change the visitor or encode the state monad
    EvaluateVisitor.env = Environment()
    return evaluate_iter(expr)