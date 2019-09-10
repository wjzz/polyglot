from parser import parse
from evaluator import evaluate

def ev(s):
    return evaluate(parse(s))

def repl():
    def print_help():
        print("Examples:\n\t2+2\n\t2 * 2 + 2")
    
    print("Evaluate simple expressions.")
    print("Type 'help' for help and 'q' or Ctrl-D to quit")
    while True:
        print("> ", end="", flush=True)
        try:
            line = input()
            line = line.strip()
            if line == "q":
                raise EOFError
            if line == "help":
                print_help()
            expr = parse(line)
            print(f"==> {evaluate(expr)}", flush=True)
        except Exception as e:
            if type(e) == EOFError:
                print("Bye!")
                break
            else:
                print(f"Failed: {e}")

if __name__ == "__main__":
    repl()
