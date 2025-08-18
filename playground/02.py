"""Generalization"""

def identity(k):
    return k

def cube(k):
    return pow(k,3)


def sum (n,term):
    """Sum the first N value of N natural numbers by function F

    >>> sum(5,cube)
    225
    """
    total, k = 0, 1
    while k<= n :
        total, k = total + term(k), k+1
    return total
