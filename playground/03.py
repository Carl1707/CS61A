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