from .utils import rand
import random


class ArrayGen:
    @staticmethod
    def gen_permutation(n: int):
        """
        Generate a random permutation of a specified length.

        Parameters:
            - `n` (int): Length of the permutation.

        Returns:
            - list: The generated random permutation.

        Examples:
            >>> ArrayGen.gen_permutation(3)
            [2, 1, 3]
        """
        return rand.gen_permutation(n)

    @staticmethod
    def identity_permutation(n: int):
        """
        Generate the identity permutation of a specified length.

        Parameters:
            - `n` (int): Length of the permutation.

        Returns:
            - list: The identity permutation.

        Examples:
            >>> ArrayGen.identity_permutation(3)
            [1, 2, 3]
        """
        return rand.identity_permutation(n)

    @staticmethod
    def gen_list(n: int, f):
        """
        Generate a list of evaluated values using a specified function.

        Parameters:
            - `n` (int): Length of the generated list.
            - `f`: The function or value to evaluate.

        Returns:
            - list: The list of evaluated results.

        Examples:
            >>> ArrayGen.gen_list(5, 10)
            [10, 10, 10, 10, 10]
        """
        return [rand.evaluate(f) for _ in range(n)]

    @staticmethod
    def gen_matrix(n: int, m: int, f):
        """
        Generate a 2D matrix of evaluated values using a specified function.

        Parameters:
            - `n` (int): Number of rows in the matrix.
            - `m` (int): Number of columns in the matrix.
            - `f`: The function or value to evaluate.

        Returns:
            - list of lists: The 2D matrix of evaluated results.

        Examples:
            >>> ArrayGen.gen_matrix(3, 2, 10)
            [[10, 10], [10, 10], [10, 10]]
        """
        return [ArrayGen.gen_list(m, f) for _ in range(n)]

    @staticmethod
    def universe_sample(m: int, l: int, r: int = None):
        """
        Generate a random sample of size m from the universe [l, r].

        Parameters:
            - `m` (int): Size of the sample.
            - `l` (int): Lower bound of the universe.
            - `r` (int, optional): Upper bound of the universe (default is None, and l becomes 0, and r becomes l).

        Returns:
            - list: A random sample of size m from the universe [l, r].

        Raises:
            - ValueError: If m is greater than the size of the population or if m is negative.

        References:
            - Exercise 5.3-5, Introduction to Algorithms 4th Edition.
        """
        if r is None:
            l, r = 0, l
        if m < 0 or m > r - l + 1:
            raise ValueError("Sample size is larger than the population or is negative")
        n = r - l + 1
        st = set()
        for k in range(n - m, n):
            i = random.randint(0, k)
            if i + l in st:
                st.add(k + l)
            else:
                st.add(i + l)
        a = list(st)
        random.shuffle(a)
        return a

    @staticmethod
    def partition(m: int, n: int):
        if m <= 0:
            raise ValueError("The number of parts must be positive: {}".format(m))
        if n < m:
            raise ValueError("Cannot split {} into {} positive parts".format(n, m))
        a = [0] + sorted(ArrayGen.universe_sample(m - 1, 1, n - 1)) + [n]
        return [a[i + 1] - a[i] for i in range(m)]
