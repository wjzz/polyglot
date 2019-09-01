from parser import parse
from evaluator import evaluate

def ev(s):
    return evaluate(parse(s))
