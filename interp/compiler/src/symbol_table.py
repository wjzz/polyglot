from ast import *

from collections import defaultdict

class UnboundVariableError(Exception):
    def __init__(self, var):
        self.var = var
        # TODO: add a line marker

class SymbolTableBuilderVisitor:
    def __init__(self):
        self._vars = defaultdict(int)
        self._current_scope = set()

    @property
    def vars(self):
        return self._vars

    @property
    def current_scope(self):
        return self._current_scope

    def visit_ArithLit(self, val):
        pass

    def visit_Var(self, var):
        if self._vars[var] == 0:
            raise UnboundVariableError(var=var)

    def visit_ArithBinop(self, op, a1, a2):
        a1.accept(self)
        a2.accept(self)

    def visit_BoolArithCmp(self, op, a1, a2):
        a1.accept(self)
        a2.accept(self)

    def visit_BoolNeg(self, b):
        b.accept(self)

    def visit_BoolBinop(self, op, b1, b2):
        b1.accept(self)
        b2.accept(self)

    def visit_StmDecl(self, tp, var, a):
        self._vars[var] += 1
        self._current_scope.add(var)
        if a is not None:
            a.accept(self)

    def visit_StmAssign(self, var, a):
        if self._vars[var] == 0:
            raise UnboundVariableError(var)
        a.accept(self)

    def visit_StmIf(self, b, ss1, ss2):
        b.accept(self)
        self.visit_many(ss1)
        self.visit_many(ss2)
    
    def visit_StmWhile(self, b, ss):
        b.accept(self)
        self.visit_many(ss)

    def visit_StmPrint(self, a):
        a.accept(self)

    def visit_many(self, stms):
        symbols = self._vars.copy()
        for stm in stms:
            stm.accept(self)
        self._vars = symbols

    def visit_StmBlock(self, stms):
        self.visit_many(stms)

def build(stms):
    """
    Builds a symbol table of all identifiers in the program.
    """
    visitor = SymbolTableBuilderVisitor()
    visitor.visit_many(stms)
    return visitor.current_scope
