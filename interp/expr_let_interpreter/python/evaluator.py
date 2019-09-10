from expr import Op

class EvaluateVisitor:
    @staticmethod
    def literal(n):
        return n
    
    @staticmethod
    def variable(v):
        ...

    @staticmethod
    def binary(e1, op, e2):
        v1 = evaluate(e1)
        v2 = evaluate(e2)
        if op == Op.Plus:
            return v1 + v2
        elif op == Op.Mult:
            return v1 * v2
    
    @staticmethod
    def let(v, e1, e2):
        ...

def evaluate(expr):
    return expr.accept_visitor(EvaluateVisitor)
