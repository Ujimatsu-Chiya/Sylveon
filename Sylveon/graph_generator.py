import random

from .graph import Graph


def _make_graph(n, *, weighted=None, directed=False, self_loop=False, multi_edge=False):
    return Graph(
        n,
        weighted=weighted,
        directed=directed,
        self_loop=self_loop,
        multi_edge=multi_edge,
    )


def _edge_capacity(n, directed=False, self_loop=False, multi_edge=False):
    if n <= 0:
        return 0
    if multi_edge:
        if self_loop:
            return None
        return None if n > 1 else 0
    if directed:
        return n * n if self_loop else n * (n - 1)
    return n * (n + 1) // 2 if self_loop else n * (n - 1) // 2


def _validate_edge_count(n, m, directed=False, self_loop=False, multi_edge=False):
    if m < 0:
        raise ValueError("Edge count must be non-negative: {}".format(m))
    capacity = _edge_capacity(n, directed, self_loop, multi_edge)
    if capacity is not None and m > capacity:
        raise ValueError("Cannot generate {} edges with n={} under the current graph constraints".format(m, n))
    if capacity == 0 and m > 0:
        raise ValueError("Cannot generate edges with n={} under the current graph constraints".format(n))


def _upper_triangle_pair(k, n, include_diagonal=False):
    left, right = 1, n
    while left < right:
        mid = (left + right) // 2
        if include_diagonal:
            through_mid = mid * (n + 1) - mid * (mid + 1) // 2
        else:
            through_mid = mid * n - mid * (mid + 1) // 2
        if through_mid <= k:
            left = mid + 1
        else:
            right = mid
    u = left
    rows = u - 1
    if include_diagonal:
        before = rows * (n + 1) - rows * (rows + 1) // 2
        v = u + (k - before)
    else:
        before = rows * n - rows * (rows + 1) // 2
        v = u + 1 + (k - before)
    return u, v


def _edge_from_index(k, n, directed=False, self_loop=False):
    if directed:
        if self_loop:
            return k // n + 1, k % n + 1
        u = k // (n - 1) + 1
        v = k % (n - 1) + 1
        if v >= u:
            v += 1
        return u, v
    return _upper_triangle_pair(k, n, self_loop)


def _random_edge(n, directed=False, self_loop=False):
    if n <= 0:
        raise ValueError("The number of vertices must be positive: {}".format(n))
    if self_loop:
        return random.randint(1, n), random.randint(1, n)
    if n < 2:
        raise ValueError("Cannot generate a non-self-loop edge with fewer than 2 vertices")
    u = random.randint(1, n)
    v = random.randint(1, n - 1)
    if v >= u:
        v += 1
    return u, v


def _fill_random_edges(g, n, m, *, directed=False, self_loop=False, multi_edge=False):
    _validate_edge_count(n, m, directed, self_loop, multi_edge)
    if multi_edge:
        while g.edge_num() < m:
            g.add_edge(*_random_edge(n, directed, self_loop))
        return
    attempts = 0
    max_attempts = max(1000, (m - g.edge_num()) * 20)
    while g.edge_num() < m and attempts < max_attempts:
        attempts += 1
        g.add_edge(*_random_edge(n, directed, self_loop))
    if g.edge_num() == m:
        return
    capacity = _edge_capacity(n, directed, self_loop, multi_edge)
    for k in random.sample(range(capacity), capacity):
        if g.edge_num() == m:
            break
        g.add_edge(*_edge_from_index(k, n, directed, self_loop))


class GraphGen:

    @staticmethod
    def gen_undirected(n, m, *, weighted=None, directed=False, self_loop=False, multi_edge=False):
        _validate_edge_count(n, m, directed, self_loop, multi_edge)
        g = _make_graph(n, weighted=weighted, directed=directed, self_loop=self_loop, multi_edge=multi_edge)
        _fill_random_edges(g, n, m, directed=directed, self_loop=self_loop, multi_edge=multi_edge)
        return g

    @staticmethod
    def gen_undirected2(n, m, *, weighted=None, directed=False, self_loop=False, multi_edge=False):
        if m < n - 1:
            raise ValueError("A connected graph with {} vertices needs at least {} edges".format(n, n - 1))
        _validate_edge_count(n, m, directed, self_loop, multi_edge)
        g = GraphGen.gen_tree(n, weighted=weighted, directed=directed, self_loop=self_loop, multi_edge=multi_edge)
        _fill_random_edges(g, n, m, directed=directed, self_loop=self_loop, multi_edge=multi_edge)
        return g

    @staticmethod
    def gen_deg_tree(n, deg=2):
        if deg <= 0:
            raise ValueError("deg must be positive: {}".format(deg))
        mp = [[-1 for _ in range(deg)] for _ in range(n + 1)]
        for i in range(2, n + 1):
            while True:
                x = random.randint(1, i - 1)
                f = random.randint(0, deg - 1)
                if mp[x][f] == -1:
                    mp[x][f] = i
                    break
        return mp

    @staticmethod
    def gen_cycle(n, *, weighted=None, directed=False, self_loop=False, multi_edge=False):
        """
        Generate a cycle graph with n vertices.

        Parameters:
            - `n` (int): Number of vertices in the cycle.
            - Graph options such as `directed`, `weighted`, `self_loop`, and `multi_edge`.

        Returns:
            - Graph: The generated cycle graph.

        Examples:
            >>> cycle_graph = GraphGen.gen_cycle(5, directed=True, weighted=[lambda: 1])
        """
        g = _make_graph(n, weighted=weighted, directed=directed, self_loop=self_loop, multi_edge=multi_edge)
        for i in range(1, n):
            g.add_edge(i, i + 1)
        g.add_edge(n, 1)
        return g

    @staticmethod
    def gen_grid(r, c, *, weighted=None, directed=False, self_loop=False, multi_edge=False):
        """
        Generate a grid graph with r rows and c columns.

        Parameters:
            - `r` (int): Number of rows in the grid.
            - `c` (int): Number of columns in the grid.
            - Graph options such as `directed`, `weighted`, `self_loop`, and `multi_edge`.

        Returns:
            - Graph: The generated grid graph.

        Examples:
            >>> grid_graph = GraphGen.gen_grid(3, 4)
        """
        if r <= 0 or c <= 0:
            raise ValueError("Grid dimensions must be positive: ({}, {})".format(r, c))
        g = _make_graph(r * c, weighted=weighted, directed=directed, self_loop=self_loop, multi_edge=multi_edge)
        for i in range(1, r + 1):
            for j in range(1, c + 1):
                u = (i - 1) * c + j
                if j < c:
                    g.add_edge(u, u + 1)
                if i < r:
                    g.add_edge(u, u + c)
        return g

    @staticmethod
    def gen_wheel(n, *, weighted=None, directed=False, self_loop=False, multi_edge=False):
        """
        Generate a wheel graph with n spokes.

        Parameters:
            - `n` (int): Number of spokes in the wheel.
            - Graph options such as `directed`, `weighted`, `self_loop`, and `multi_edge`.

        Returns:
            - Graph: The generated wheel graph.

        Examples:
            >>> wheel_graph = GraphGen.gen_wheel(6, weighted=[lambda: 2])

        Raises:
            - ValueError: If n is less than 4.
        """
        if n < 4:
            raise ValueError("A wheel graph has at least 4 nodes. The n you provided is: {}".format(n))
        g = _make_graph(n, weighted=weighted, directed=directed, self_loop=self_loop, multi_edge=multi_edge)
        for i in range(2, n + 1):
            g.add_edge(1, i)
        for i in range(3, n + 1):
            g.add_edge(i - 1, i)
        g.add_edge(2, n)
        return g

    @staticmethod
    def gen_chain(n, *, weighted=None, directed=False, self_loop=False, multi_edge=False):
        """
        Generate a chain graph with n vertices.

        Parameters:
            - `n` (int): Number of vertices in the chain.
            - Graph options such as `directed`, `weighted`, `self_loop`, and `multi_edge`.

        Returns:
            - Graph: The generated chain graph.

        Examples:
            >>> chain_graph = GraphGen.gen_chain(5, directed=True, weighted=[lambda: 1])
        """
        return GraphGen.gen_tree(n, chain_rate=1.0, weighted=weighted, directed=directed,
                                 self_loop=self_loop, multi_edge=multi_edge)

    @staticmethod
    def gen_star(n, *, weighted=None, directed=False, self_loop=False, multi_edge=False):
        """
        Generate a star graph with n vertices.

        Parameters:
            - `n` (int): Number of vertices in the star.
            - Graph options such as `directed`, `weighted`, `self_loop`, and `multi_edge`.

        Returns:
            - Graph: The generated star graph.

        Examples:
            >>> star_graph = GraphGen.gen_star(5, weighted=[lambda: 2])

        Raises:
            - ValueError: If n is less than 3.
        """
        return GraphGen.gen_tree(n, star_rate=1.0, weighted=weighted, directed=directed,
                                 self_loop=self_loop, multi_edge=multi_edge)

    @staticmethod
    def gen_tree(n, chain_rate: float = 0, star_rate: float = 0, *, weighted=None,
                 directed=False, self_loop=False, multi_edge=False):
        """
        Generate a tree graph with n vertices.

        Parameters:
            - `n` (int): Number of vertices in the tree.
            - `chain_rate` (float): Proportion of edges forming a chain in the tree (default is 0).
            - `star_rate` (float): Proportion of edges forming a star in the tree (default is 0).
            - Graph options such as `directed`, `weighted`, `self_loop`, and `multi_edge`.

        Returns:
            - Graph: The generated tree graph.

        Examples:
            >>> tree_graph = GraphGen.gen_tree(6, chain_rate=0.5, weighted=[lambda: 1])

        Raises:
            - ValueError: If the sum of chain_rate and star_rate is greater than 1.
        """
        if not 0 <= chain_rate <= 1 or not 0 <= star_rate <= 1 or not 0 <= chain_rate + star_rate <= 1:
            raise ValueError('''The parameters chain_rate and star_rate must meet the following conditions:
- 0 <= chain_rate <= 1
- 0 <= star_rate <= 1
- 0 <= chain_rate + star_rate <= 1
The chain_rate and star_rate you provided are {} and {} respectively.
            '''.format(chain_rate, star_rate))
        m = n - 1
        chain_edges = round(m * chain_rate)
        star_edges = round(m * star_rate)
        if chain_edges > m:
            chain_edges = m
        if chain_edges + star_edges > m:
            star_edges = m - chain_edges
        g = _make_graph(n, weighted=weighted, directed=directed, self_loop=self_loop, multi_edge=multi_edge)
        for i in range(star_edges):
            g.add_edge(1, i + 2)
        for i in range(chain_edges):
            g.add_edge(star_edges + i + 1, star_edges + i + 2)
        for i in range(chain_edges + star_edges + 1, n):
            g.add_edge(random.randint(1, i), i + 1)
        return g

    @staticmethod
    def gen_DAG(n, m, *, weighted=None):
        if m < 0:
            raise ValueError("Edge count must be non-negative: {}".format(m))
        capacity = n * (n - 1) // 2
        if m > capacity:
            raise ValueError("Cannot generate {} DAG edges with n={}; maximum is {}".format(m, n, capacity))
        g = _make_graph(n, weighted=weighted, directed=True)
        for k in random.sample(range(capacity), m):
            x, y = _upper_triangle_pair(k, n)
            g.add_edge(x, y)
        return g


def to_root(ls, st: int = None):
    from collections import deque
    n = len(ls) + 1
    g = [[] for _ in range(n)]
    for x, y in ls:
        g[x].append(y)
        g[y].append(x)
    pre = [None for _ in range(n)]
    if st is None:
        st = random.randint(0, n - 1)
    pre[st] = -1
    q = deque([st])
    while q:
        u = q.popleft()
        for v in g[u]:
            if pre[v] is None:
                pre[v] = u
                q.append(v)
    return pre
