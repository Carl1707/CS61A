def fizzbuzz(n):
    """
    >>> result = fizzbuzz(16)
    1
    2
    fizz
    4
    buzz
    fizz
    7
    8
    fizz
    buzz
    11
    fizz
    13
    14
    fizzbuzz
    16
    >>> print(result)
    None
    """
    k=1
    while k <= n :
        if k % 3 == 0 and k % 5 != 0 :
            print ('fizz')
        elif k % 3 != 0 and k % 5 == 0 :
            print ('buzz')
        elif k % 3 == 0 and k % 5 == 0 :
            print('fizzbuzz')
        else :
            print (k)
        k += 1

def is_prime(n):
    """
    >>> is_prime(10)
    False
    >>> is_prime(7)
    True
    >>> is_prime(1) # one is not a prime number!!
    False
    """
    assert n > 0 , 'n must be positive'
    count , k = 0 , 1
    while k <= n :
        if n % k ==0 :
            count += 1
        k += 1
    if count == 2 :
        return True
    elif count == 1 :
        return  False
    else :
        return False

def unique_digits(n):
    """Return the number of unique digits in positive integer n.

    >>> unique_digits(8675309) # All are unique
    7
    >>> unique_digits(13173131) # 1, 3, and 7
    3
    >>> unique_digits(101) # 0 and 1
    2
    """
    count , k = 0 , 0
    while k <= 9 :
        if has_digit(n,k) :
            count += 1
        k += 1
    return count

def has_digit(n, k):
    """Returns whether k is a digit in n.

    >>> has_digit(10, 1)
    True
    >>> has_digit(12, 7)
    False
    """
    assert k >= 0 and k < 10
    while n > 0 :
        if n % 10 == k :
            return True
        else :
            n = n // 10
    if n == 0 :
        return False

def ordered_digits(x):
    """Return True if the (base 10) digits of X>0 are in non-decreasing
    order, and False otherwise.

    >>> ordered_digits(5)
    True
    >>> ordered_digits(11)
    True
    >>> ordered_digits(127)
    True
    >>> ordered_digits(1357)
    True
    >>> ordered_digits(21)
    False
    >>> result = ordered_digits(1375) # Return, don't print
    >>> result
    False
    """
    pre , cur = 10 , 0
    while x > 0 :
        cur = x % 10
        if cur <= pre :
            pre = cur
            x = x // 10
        else :
            return False
    return True