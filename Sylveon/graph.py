from .utils.rand import gen_permutation, evaluate_list, int_1bit
import random
from collections import defaultdict


class Edge:
    def __init__(self, u, v, weight_list: list = None):
        """
        Initialize an Edge object.

        Parameters:
            - `u` (int): Starting vertex of the edge.
            - `v` (int): Ending vertex of the edge.
            - `weight_list` (list, optional): List of weights for the edge (default is an empty list).
        """
        if weight_list is None:
            weight_list = []
        self.start = u
        self.end = v
        self.weight_list = weight_list

    def __str__(self):
        """
        Generate a string representation of the edge.

        Returns:
            - str: String representation of the edge.
        """
        return self.format()

    def __repr__(self):
        """
        Generate a string representation of the edge for debugging.

        Returns:
            - str: String representation of the edge for debugging purposes.
        """
        return "(" + " ".join(map(str, [self.start, self.end] + self.weight_list)) + ")"

    def __iter__(self):
        return iter(self.to_list())

    def to_list(self):
        return [self.start, self.end] + self.weight_list

    def format(self, separator=" "):
        return separator.join(map(str, self.to_list()))


class Graph:
    def __init__(self, n: int, *, weighted=None, directed: bool = False,
                 self_loop: bool = False, multi_edge: bool = False):
        """
        Initialize a Graph object.

        Parameters:
            - `n` (int): The number of vertices in the graph.
            - `weighted` (list, optional): List of weight functions for edges (default is an empty list).
            - `directed` (bool, optional): Whether the graph is directed (default is False).
            - `self_loop` (bool, optional): Whether to allow self-loops (default is False).
            - `multi_edge` (bool, optional): Whether to allow multiple edges between the same vertices (default is False).
        """
        if weighted is None:
            weighted = []
        self.n = n
        self.__m = 0
        self.weight_func_list = weighted
        self.directed = directed
        self.self_loop = self_loop
        self.multi_edge = multi_edge
        self.__edge_list = [defaultdict(list) for _ in range(n + 1)]

    def edge_num(self):
        """
        Get the number of edges in the graph.

        Returns:
            - int: The number of edges in the graph.
        """
        return self.__m

    def __iterator_edge(self):
        for start in range(1, self.n + 1):
            for end, edge_list in self.__edge_list[start].items():
                if start <= end or self.directed:
                    for edge in edge_list:
                        yield edge

    def __has_edge(self, u, v):
        return v in self.__edge_list[u]

    def add_edge(self, u, v):
        """
        Add an edge to the graph.

        Parameters:
            - `u` (int): Starting vertex of the edge.
            - `v` (int): Ending vertex of the edge.
        """
        if not 1 <= u <= self.n or not 1 <= v <= self.n:
            raise ValueError("Vertex index out of range: ({}, {}) for graph with {} vertices".format(u, v, self.n))
        if not self.self_loop and u == v:
            return False
        if not self.multi_edge and self.__has_edge(u, v):
            return False
        self.__m += 1
        w = evaluate_list(self.weight_func_list)
        self.__edge_list[u][v].append(Edge(u, v, w))
        if not self.directed and u != v:
            self.__edge_list[v][u].append(Edge(v, u, w))
        return True

    def __build_edge_output(self, *, first_index=1, shuffle_edges=True,
                            shuffle_vertices=True, flip_undirected_edges=True):
        output = [Edge(e.start, e.end, list(e.weight_list)) for e in self.__iterator_edge()]
        if shuffle_edges:
            random.shuffle(output)
        if shuffle_vertices:
            permutation = gen_permutation(self.n)
            for edge in output:
                edge.start = permutation[edge.start - 1]
                edge.end = permutation[edge.end - 1]
        if flip_undirected_edges and not self.directed:
            for edge in output:
                if int_1bit():
                    edge.start, edge.end = edge.end, edge.start
        for edge in output:
            edge.start += first_index - 1
            edge.end += first_index - 1
        return output

    def to_edge_list(self, *, first_index=1, shuffle_edges=True,
                     shuffle_vertices=True, flip_undirected_edges=True):
        """
        Return the graph as an edge list.
        """
        output = self.__build_edge_output(first_index=first_index, shuffle_edges=shuffle_edges,
                                          shuffle_vertices=shuffle_vertices,
                                          flip_undirected_edges=flip_undirected_edges)
        return [edge.to_list() for edge in output]

    def to_matrix(self):
        """
        Return the graph as an adjacency matrix.
        """
        if self.n > 10000:
            print("n is too large. {}".format(self.n))
        mat = [[0 for _ in range(self.n)] for _ in range(self.n)]
        for edge in self.__iterator_edge():
            start, end = edge.start - 1, edge.end - 1
            mat[start][end] = 1
            if not self.directed:
                mat[end][start] = 1
        return mat

    def to_string(self, *, separator=" ", first_index=1, shuffle_edges=True,
                  shuffle_vertices=True, flip_undirected_edges=True):
        """
        Return the graph edge list as formatted text.
        """
        output = self.__build_edge_output(first_index=first_index, shuffle_edges=shuffle_edges,
                                          shuffle_vertices=shuffle_vertices,
                                          flip_undirected_edges=flip_undirected_edges)
        return "\n".join(edge.format(separator) for edge in output)

    def to_matrix_string(self, *, separator=""):
        """
        Return the adjacency matrix as formatted text.
        """
        return "\n".join(separator.join(str(v) for v in line) for line in self.to_matrix())

    def __str__(self):
        """
        Generate a string representation of the graph.

        Returns:
            - str: String representation of the graph.
        """
        return self.to_string()

    def __repr__(self):
        """
        Generate a string representation of the graph for debugging.

        Returns:
            - str: String representation of the graph for debugging purposes.
        """
        return "edge_list: {}".format(list(self.__iterator_edge()))
