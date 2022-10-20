import numpy as np


def printargs(*args, **kwargs):
    print("args")
    for a in args:
        print(a)
    for kw in kwargs:
        print(f"{kw} : {kwargs[kw]}")


def printstate(state):
    print("\nreading state: ")
    for s in state:
        print(f"key={s}, value ={state[s]}")


def to_none(state):
    for s in state:
        state[s] = None


def addfoo(state):
    state["foo"] = 3


def remove(state):
    state = {}


def to_zero_values(state):
    for a in state:
        if isinstance(state[a], np.ndarray):
            state[a] = np.zeros(state[a].shape)


def get_max(state):
    for v in state.values():
        if isinstance(v, np.ndarray):
            return np.max(v)
