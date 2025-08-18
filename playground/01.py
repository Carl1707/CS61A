"""Our first Python source file."""

from operator import floordiv,mod

def div_exact(n,d):
    """Return the quotient and remainder of dividing N by D.

    >>> q, r = div_exact(2025,10)
    >>> q
    202
    >>> r
    6
    """
    return floordiv(n,d),mod(n,d)

