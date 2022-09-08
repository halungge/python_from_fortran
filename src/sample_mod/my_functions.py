def sumup(limit: int) -> int:
    res = sum(range(limit + 1))
    print(f"python-print: summing up to {limit} = {res}")
    return res


def hello_world():
    print("python-print: hello world")


def say_hello(name: str):
    print(f"hello {name}")


def print_args(*args, **kwargs) -> str:
    print("python-print")
    print("   ---> Arguments: ", args)
    print("   ---> Keyword arguments: ", kwargs)
    return "done sample_functions.print_args"
