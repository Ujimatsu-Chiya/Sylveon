import random


class MazeGen:
    @staticmethod
    def __gen_recursive_backtracking_core(n, m, **kwargs):
        """
        Generate a maze using the Recursive Backtracking algorithm.

        Parameters:
            - `n` (int): Number of rows in the maze.
            - `m` (int): Number of columns in the maze.
            - `**kwargs`: Additional keyword arguments.
                - `shuffle_dir` (bool): Whether to shuffle the direction order (default is True).

        Returns:
            - list of lists: The generated maze represented as a 2D matrix.
        """
        maze = [[1 for _ in range(m)] for _ in range(n)]
        shuffle_dir = kwargs.get("shuffle_dir", True)

        def is_valid(x, y):
            return 0 <= x < n and 0 <= y < m and maze[x][y] == 1

        def dfs(x, y):
            dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            if shuffle_dir:
                random.shuffle(dir)
            for dx, dy in dir:
                nx, ny = x + dx, y + dy
                if is_valid(nx * 2, ny * 2):
                    maze[nx * 2][ny * 2] = maze[x * 2 + dx][y * 2 + dy] = 0
                    dfs(nx, ny)

        sx, sy = random.randint(0, (n - 1) // 2), random.randint(0, (m - 1) // 2)
        maze[sx * 2][sy * 2] = 0
        dfs(sx, sy)
        return maze

    @staticmethod
    def __gen_recursive_division_core(n, m, **kwargs):
        """
        Generate a maze using the Recursive Division algorithm.

        Parameters:
            - `n` (int): Number of rows in the maze.
            - `m` (int): Number of columns in the maze.
            - `**kwargs`: Additional keyword arguments.

        Returns:
            - list of lists: The generated maze represented as a 2D matrix.
        """
        maze = [[1 for _ in range(m)] for _ in range(n)]

        def divide(xa, ya, xb, yb):
            if xa == xb and ya == yb:
                return
            cnt_x, cnt_y = xb - xa, yb - ya
            k = random.randint(0, cnt_x + cnt_y - 1)
            if k < cnt_x:
                xm = xa + k
                y_choose = random.randint(ya, yb)
                maze[xm * 2 + 1][y_choose * 2] = 0
                divide(xa, ya, xm, yb)
                divide(xm + 1, ya, xb, yb)
            else:
                k -= cnt_x
                ym = ya + k
                x_choose = random.randint(xa, xb)
                maze[x_choose * 2][ym * 2 + 1] = 0
                divide(xa, ya, xb, ym)
                divide(xa, ym + 1, xb, yb)

        ex, ey = (n - 1) // 2, (m - 1) // 2
        divide(0, 0, ex, ey)

        for i in range(ex + 1):
            for j in range(ey + 1):
                maze[i * 2][j * 2] = 0
        return maze

    @staticmethod
    def __gen_prim_core(n, m, **kwargs):
        """
        Generate a maze using the Prim's algorithm.

        Parameters:
            - `n` (int): Number of rows in the maze.
            - `m` (int): Number of columns in the maze.
            - `**kwargs`: Additional keyword arguments.
                - `shuffle_dir` (bool): Whether to shuffle the direction order (default is True).

        Returns:
            - list of lists: The generated maze represented as a 2D matrix.
        """
        maze = [[1 for _ in range(m)] for _ in range(n)]

        def is_valid(x, y):
            return 0 <= x < n and 0 <= y < m and maze[x][y] == 1

        sx, sy = random.randint(0, (n - 1) // 2), random.randint(0, (m - 1) // 2)
        maze[sx][sy] = 0
        dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        shuffle_dir = kwargs.get("shuffle_dir", True)
        ls = [(sx, sy)]
        while len(ls) > 0:
            pos = random.randint(0, len(ls) - 1)
            x, y = ls[pos]
            ls[pos] = ls[-1]
            ls.pop()
            if shuffle_dir:
                random.shuffle(dir)
            for dx, dy in dir:
                nx, ny = x + dx, y + dy
                if is_valid(nx * 2, ny * 2):
                    maze[nx * 2][ny * 2] = maze[x * 2 + dx][y * 2 + dy] = 0
                    ls.append((nx, ny))

        return maze

    @staticmethod
    def __gen_kruskal_core(n, m, **kwargs):
        """
        Generate a maze using the Kruskal's algorithm.

        Parameters:
            - `n` (int): Number of rows in the maze.
            - `m` (int): Number of columns in the maze.
            - `**kwargs`: Additional keyword arguments.

        Returns:
            - list of lists: The generated maze represented as a 2D matrix.
        """
        maze = [[1 for _ in range(m)] for _ in range(n)]
        ex, ey = (n - 1) // 2, (m - 1) // 2
        fa = [[(i, j) for j in range(ey + 1)] for i in range(ex + 1)]

        def find(x, y):
            if fa[x][y] == (x, y):
                return fa[x][y]
            else:
                fa[x][y] = find(*fa[x][y])
                return fa[x][y]

        def merge(xa, ya, xb, yb):
            ta, tb = find(xa, ya), find(xb, yb)
            fa[ta[0]][ta[1]] = tb

        edges = []
        for i in range(ex + 1):
            for j in range(ey + 1):
                if i < ex:
                    edges.append((i, j, 0))
                if j < ey:
                    edges.append((i, j, 1))
                maze[i * 2][j * 2] = 0
        random.shuffle(edges)
        for x, y, d in edges:
            if d == 0 and find(x, y) != find(x + 1, y):
                merge(x, y, x + 1, y)
                maze[x * 2 + 1][y * 2] = 0
            elif d == 1 and find(x, y) != find(x, y + 1):
                merge(x, y, x, y + 1)
                maze[x * 2][y * 2 + 1] = 0
        return maze

    @staticmethod
    def __maze_gen_aux(n, m, maze_gen_func, *, block_to_empty_rate=0, empty_to_block_rate=0,
                       start_pos=None, end_pos=None, empty="0", block="1",
                       start_mark=None, end_mark=None, shuffle_dir=True):
        """
        Auxiliary function for generating a maze with additional features.

        Parameters:
            - `n` (int): Number of rows in the maze.
            - `m` (int): Number of columns in the maze.
            - `maze_gen_func`: The core maze generation function.
            - Maze output options such as `block_to_empty_rate`, `start_pos`, `end_pos`, and `shuffle_dir`.

        Returns:
            - str: The generated maze represented as a string.
        """
        if n <= 0 or m <= 0:
            raise ValueError("Maze dimensions must be positive: ({}, {})".format(n, m))
        if start_mark is None:
            start_mark = empty
        if end_mark is None:
            end_mark = empty
        maze = maze_gen_func(n, m, shuffle_dir=shuffle_dir)
        if start_pos is not None:
            maze[start_pos[0]][start_pos[1]] = start_mark
        if end_pos is not None:
            maze[end_pos[0]][end_pos[1]] = end_mark

        if n % 2 == 0:
            for j in range(0, m, 2):
                if maze[-2][j] == 0 and random.random() < block_to_empty_rate:
                    maze[-1][j] = 0
        if m % 2 == 0:
            for i in range(0, n, 2):
                if maze[i][-2] == 0 and random.random() < block_to_empty_rate:
                    maze[i][-1] = 0
        for i in range(n):
            for j in range(m):
                if maze[i][j] == 1 and random.random() < block_to_empty_rate:
                    maze[i][j] = 0
                elif maze[i][j] == 0 and random.random() < empty_to_block_rate:
                    maze[i][j] = 1
        for i in range(n):
            for j in range(m):
                if (i, j) == start_pos:
                    maze[i][j] = start_mark
                elif (i, j) == end_pos:
                    maze[i][j] = end_mark
                elif maze[i][j] == 0:
                    maze[i][j] = empty
                else:
                    maze[i][j] = block
        return "\n".join("".join(ch for ch in raw) for raw in maze)

    @staticmethod
    def gen_recursive_backtracking_maze(n, m, *, block_to_empty_rate=0, empty_to_block_rate=0,
                                        start_pos=None, end_pos=None, empty="0", block="1",
                                        start_mark=None, end_mark=None, shuffle_dir=True):
        """
        Generate a maze using the Recursive Backtracking algorithm with additional features.

        Parameters:
            - `n` (int): Number of rows in the maze.
            - `m` (int): Number of columns in the maze.
            - Maze output options such as `block_to_empty_rate`, `start_pos`, `end_pos`, and `shuffle_dir`.

        Returns:
            - str: The generated maze represented as a string.
        """
        return MazeGen.__maze_gen_aux(n, m, MazeGen.__gen_recursive_backtracking_core,
                                      block_to_empty_rate=block_to_empty_rate,
                                      empty_to_block_rate=empty_to_block_rate,
                                      start_pos=start_pos, end_pos=end_pos, empty=empty,
                                      block=block, start_mark=start_mark,
                                      end_mark=end_mark, shuffle_dir=shuffle_dir)

    @staticmethod
    def gen_recursive_division_maze(n, m, *, block_to_empty_rate=0, empty_to_block_rate=0,
                                    start_pos=None, end_pos=None, empty="0", block="1",
                                    start_mark=None, end_mark=None, shuffle_dir=True):
        """
        Generate a maze using the Recursive Division algorithm with additional features.

        Parameters:
            - `n` (int): Number of rows in the maze.
            - `m` (int): Number of columns in the maze.
            - Maze output options such as `block_to_empty_rate`, `start_pos`, `end_pos`, and `shuffle_dir`.

        Returns:
            - str: The generated maze represented as a string.
        """
        return MazeGen.__maze_gen_aux(n, m, MazeGen.__gen_recursive_division_core,
                                      block_to_empty_rate=block_to_empty_rate,
                                      empty_to_block_rate=empty_to_block_rate,
                                      start_pos=start_pos, end_pos=end_pos, empty=empty,
                                      block=block, start_mark=start_mark,
                                      end_mark=end_mark, shuffle_dir=shuffle_dir)

    @staticmethod
    def gen_prim_maze(n, m, *, block_to_empty_rate=0, empty_to_block_rate=0,
                      start_pos=None, end_pos=None, empty="0", block="1",
                      start_mark=None, end_mark=None, shuffle_dir=True):
        """
        Generate a maze using the Prim's algorithm with additional features.

        Parameters:
            - `n` (int): Number of rows in the maze.
            - `m` (int): Number of columns in the maze.
            - Maze output options such as `block_to_empty_rate`, `start_pos`, `end_pos`, and `shuffle_dir`.

        Returns:
            - str: The generated maze represented as a string.
        """
        return MazeGen.__maze_gen_aux(n, m, MazeGen.__gen_prim_core,
                                      block_to_empty_rate=block_to_empty_rate,
                                      empty_to_block_rate=empty_to_block_rate,
                                      start_pos=start_pos, end_pos=end_pos, empty=empty,
                                      block=block, start_mark=start_mark,
                                      end_mark=end_mark, shuffle_dir=shuffle_dir)

    @staticmethod
    def gen_kruskal_maze(n, m, *, block_to_empty_rate=0, empty_to_block_rate=0,
                         start_pos=None, end_pos=None, empty="0", block="1",
                         start_mark=None, end_mark=None, shuffle_dir=True):
        """
        Generate a maze using the Kruskal's algorithm with additional features.

        Parameters:
            - `n` (int): Number of rows in the maze.
            - `m` (int): Number of columns in the maze.
            - Maze output options such as `block_to_empty_rate`, `start_pos`, `end_pos`, and `shuffle_dir`.

        Returns:
            - str: The generated maze represented as a string.
        """
        return MazeGen.__maze_gen_aux(n, m, MazeGen.__gen_kruskal_core,
                                      block_to_empty_rate=block_to_empty_rate,
                                      empty_to_block_rate=empty_to_block_rate,
                                      start_pos=start_pos, end_pos=end_pos, empty=empty,
                                      block=block, start_mark=start_mark,
                                      end_mark=end_mark, shuffle_dir=shuffle_dir)
