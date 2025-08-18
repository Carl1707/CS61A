def tree(label, branches=[]):
    return [label] + branches

def tree(label, branches=[]):
    for branch in branches:
        assert is_tree(branch)
    # 确保branch是tree
    return [label] + list(branches)

def label(tree):
    return tree[0]  # label函数是一个选择器，返回树的列表中索引为0的元素

def branches(tree):
    return tree[1:]  # branches函数返回一个表示 列表表示下 其余元素 的列表

def is_tree(tree):
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    # 递归遍历树的每一个分支
    return True

def is_leaf(tree):
    return not branches(tree)

def fib_tree(n):
    if n <= 1:
        return tree(n)  # 只能是叶子
    else:
        left, right = fib_tree(n - 2), fib_tree(n - 1)
        return tree(label(left) + label(right), [left, right])

def count_leaves(t):
    """Count the leaves of a tree."""
    if is_leaf(t):
        return 1
    else:
        sum = 0
        for branch in branches(tree):
            sum += count_leaves(branch)
        return sum  # 要找的是叶子数目

def leaves(tree):
    if is_leaf(tree):
        return [label(tree)]
    return sum([leaves(b) for b in branches(tree)], [])

def increment_leaves(t):

    if is_leaf(t):
        return tree(label(t) + 1)
    else:
        increment_branch = [increment_leaves(b) for b in branches(t)]
        return tree(label(t), increment_branch)

def increment(t):
    increment_branch = [increment(b) for b in branches(t)]
    return tree(label(t) + 1, increment_branch)
# 到达最基本情况时，后面的for控制体对应的已经是空列表，就不会再递归调用了

def count_paths(t,total):
    if label(t) == total:
        found = 1
    else:
        found = 0
    return found + sum([count_paths(b, total - label(t)) for b in branches(t)])

def even_weighted_loop(s):
    """
    >>> x = [1, 2, 3, 4, 5, 6]
    >>> even_weighted_loop(x)
    [0, 6, 20]
    """
    new_list = []
    i = 0
    while i < len(s) :
        if i % 2 == 0 :
            new_list += [s[i] * i]
        i += 1
    return new_list

def even_weighted_comprehension(s):
    """
    >>> x = [1, 2, 3, 4, 5, 6]
    >>> even_weighted_comprehension(x)
    [0, 6, 20]
    """
    return [ s[i] * i   for  i in range(len(s)) if i % 2 == 0          ]

def happy_givers(gifts):
    """
    >>> gift_recipients = {
    ...     "Alice": "Eve", # Alice gave a gift to Eve
    ...     "Bob": "Finn",
    ...     "Christina": "Alice",
    ...     "David": "Gina", # Gina is not a key because she didn't give anyone a gift
    ...     "Eve": "Alice",
    ...     "Finn": "Bob",
    ... }
    >>> list(sorted(happy_givers(gift_recipients))) # Order does not matter
    ['Alice', 'Bob', 'Eve', 'Finn']
    """
    return [ giver for giver in list(gifts)  if  gifts[giver] in list(gifts)    and   gifts[gifts[giver]] == giver ]
    ##是否在字典中也要判断


def max_path_sum(t):
    """Return the maximum path sum of the tree.
    >>> t = tree(1, [tree(5, [tree(1), tree(3)]), tree(10)])
    >>> max_path_sum(t)
    11
    """
    def is_leaf(tree):
        return not tree[1:]
    if is_leaf(t):
        return t[0]
    else :
        return t[0] + max([ max_path_sum(branch) for branch in t[1:]])

def preorder(t):
    """Return a list of the entries in this tree in the order that they
    would be visited by a preorder traversal (see problem description).

    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> preorder(numbers)
    [1, 2, 3, 4, 5, 6, 7]
    >>> preorder(tree(2, [tree(4, [tree(6)])]))
    [2, 4, 6]
    """
    if is_leaf(t):
        return [label(t)]
    else :
        return [label(t)] + sum([preorder(branch) for branch in branches(t)], [])

def find_path(t, x):
    """
    >>> t2 = tree(5, [tree(6), tree(7)])
    >>> t1 = tree(3, [tree(4), t2])
    >>> find_path(t1, 5)
    [3, 5]
    >>> find_path(t1, 4)
    [3, 4]
    >>> find_path(t1, 6)
    [3, 5, 6]
    >>> find_path(t2, 6)
    [5, 6]
    >>> print(find_path(t1, 2))
    None
    """
    if   label(t) == x:
        return [label(t)]
    for branch in branches(t):
        path = find_path(branch, x)
        if path:
            return [label(t)] + find_path(branch, x)
    return None