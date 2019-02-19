"""Decorator for expressing tail recursive functions."""


def recur(f):
    """
    Decorator for expressing tail recursive functions.

    Does a slightly less than optimal tail call optimization
    by dropping the stack frame, then recreating (rather than
    modifying in place and jumping).
    """
    def __atom():
        """
        This isn't (easily) visible to the outside world, and hence
        won't be returned from f.
        """
        pass

    def _recur(*args, **kwargs):
        """
        Recur passes back a marked (identifiable) continuation
        to allow the stack frame to be eliminated.
        """
        return (__atom, lambda: f(_recur, *args, **kwargs))

    def wrapped(*args, **kwargs):
        """Iterate with f until there is no continuation."""

        def has_continuation(v):
            """Decide whether _recur was called."""
            return isinstance(v, tuple) and len(v) > 0 and v[0] == __atom

        res = f(_recur, *args, **kwargs)
        while has_continuation(res):
            _, cont = res
            res = cont()

        return res

    return wrapped
