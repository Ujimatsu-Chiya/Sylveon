from .array_generator import ArrayGen
from .io_file import *
from .graph_generator import *
from .maze_generator import MazeGen
from .string_generator import StringGen
from .graph import Graph
from .utils.rand import *

from random import randint, uniform, random, choices, sample


class Gen(ArrayGen, GraphGen, StringGen, MazeGen):
    pass


def bracket_list(n):
    res = []
    l = n
    r = 0
    for _ in range(n + n):
        x = randint(1, l + r)
        if x <= l:
            res.append(1)
            l -= 1
            r += 1
        else:
            res.append(-1)
            r -= 1
    return res
