from recur.recur import recur
from functools import reduce


def test_factorial():

    def factorial(n):
        """Factorial of n."""
        @recur
        def f(recur, acc, n):
            """Tail recursive factorial function."""
            if n == 0:
                return acc
            else:
                return recur(n * acc, n - 1)

        return f(1, n)

    def oracle(n):
        return reduce(lambda x, y: x * y, range(1, n + 1))

    assert factorial(3) == 6
    assert factorial(10) == oracle(10)
    assert factorial(1000) == oracle(1000)
    assert factorial(10000) == oracle(10000)


def test_wrapped_is_contained():

    def factorial(n):
        @recur
        def f(recur, acc, n):
            if n == 0:
                return (f, acc)
            else:
                return recur(n * acc, n - 1)

        _, v = f(1,n)
        return v

    assert factorial(3) == 6


def test_recur_is_contained():

    def factorial(n):
        @recur
        def f(recur, acc, n):
            if n == 0:
                return (recur, acc)
            else:
                return recur(n * acc, n - 1)

        _, v = f(1,n)
        return v

    assert factorial(3) == 6


def test_empty_tuple_is_contained():

    @recur
    def f(recur):
        return ()

    f()
