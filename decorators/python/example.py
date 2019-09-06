def example(fun):
    print("Applying the wrapper")

    def wrapper(*args, **kwargs):
        print("Running the wrapped function")
        value = fun(*args, **kwargs)
        print("Calculation done!")
        return value
    
    # it's good practice to do this
    wrapper.__name__ = fun.__name__
    return wrapper

@example
def hello():
    print("hello!")

if __name__ == "__main__":
    hello()
    print(hello.__name__)
