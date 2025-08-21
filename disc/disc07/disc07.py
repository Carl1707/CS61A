from tables.nodes.filenode import new_node


def is_bst(t):
    """Returns True if the Tree t has the structure of a valid BST.
    >>> t1 = Tree(6, [Tree(2, [Tree(1), Tree(4)]), Tree(7, [Tree(7), Tree(8)])])
    >>> is_bst(t1)
    True
    >>> t2 = Tree(8, [Tree(2, [Tree(9), Tree(1)]), Tree(3, [Tree(6)]), Tree(5)])
    >>> is_bst(t2)
    False
    >>> t3 = Tree(6, [Tree(2, [Tree(4), Tree(1)]), Tree(7, [Tree(7), Tree(8)])])
    >>> is_bst(t3)
    False
    >>> t4 = Tree(1, [Tree(2, [Tree(3, [Tree(4)])])])
    >>> is_bst(t4)
    True
    >>> t5 = Tree(1, [Tree(0, [Tree(-1, [Tree(-2)])])])
    >>> is_bst(t5)
    True
    >>> t6 = Tree(1, [Tree(4, [Tree(2, [Tree(3)])])])
    >>> is_bst(t6)
    True
    >>> t7 = Tree(2, [Tree(1, [Tree(5)]), Tree(4)])
    >>> is_bst(t7)
    False
    """
    def bst_min(t):
        if t.is_leaf:
            return t.label
        else:
            return min([bst_min(b) for b in t.branches])

    def bst_max(t):
        if t.is_leaf:
            return t.label
        else:
            return max([bst_max(b) for b in t.branches])

    if t.is_leaf:
        return True
    else:
        if len(t.branches) == 2:
            return bst_max(t.branches[0]) <= t.label < bst_min(t.branches[1]) and is_bst(t.branches[0]) and is_bst(t.branches[1])
        elif len(t.branches) == 1:
            if t.branches[0].label > t.label:
                return t.label < bst_min(t.branches[0]) and is_bst(t.branches[0])
            else:
                return t.label >= bst_max(t.branches[0]) and is_bst(t.branches[0])
        else:
            return False


# --- 优化后的 is_bst 函数 ---
# 使用有效范围来判断
# def is_bst(t):
#     """
#     Returns True if the Tree t has the structure of a valid BST.
#     >>> t1 = Tree(6, [Tree(2, [Tree(1), Tree(4)]), Tree(7, [Tree(7), Tree(8)])])
#     >>> is_bst(t1)
#     True
#     >>> t2 = Tree(8, [Tree(2, [Tree(9), Tree(1)]), Tree(3, [Tree(6)]), Tree(5)])
#     >>> is_bst(t2)
#     False
#     >>> t3 = Tree(6, [Tree(2, [Tree(4), Tree(1)]), Tree(7, [Tree(7), Tree(8)])])
#     >>> is_bst(t3)
#     False
#     >>> t4 = Tree(1, [Tree(2, [Tree(3, [Tree(4)])])])
#     >>> is_bst(t4)
#     True
#     >>> t5 = Tree(1, [Tree(0, [Tree(-1, [Tree(-2)])])])
#     >>> is_bst(t5)
#     True
#     >>> t6 = Tree(1, [Tree(4, [Tree(2, [Tree(3)])])])
#     >>> is_bst(t6)
#     True
#     >>> t7 = Tree(2, [Tree(1, [Tree(5)]), Tree(4)])
#     >>> is_bst(t7)
#     False
#     """
#     def is_bst_helper(t, min_val, max_val):
#         """
#         A helper function that checks if a tree is a valid BST
#         within the given (min_val, max_val) range.
#         """
#         # 1. 检查当前节点的值是否在有效范围内
#         if not (min_val < label(t) < max_val):
#             return False
#
#         # 2. 根据树的结构递归检查分支
#         if is_leaf(t):
#             return True
#         elif len(branches(t)) == 1:
#             # 假设分支[0]是左子树
#             if label(branches(t)[0]) < label(t):
#                 # 递归检查左子树，更新上界为当前节点的值
#                 return is_bst_helper(branches(t)[0], min_val, label(t))
#             # 假设分支[0]是右子树
#             else:
#                 # 递归检查右子树，更新下界为当前节点的值
#                 return is_bst_helper(branches(t)[0], label(t), max_val)
#         elif len(branches(t)) == 2:
#             left, right = branches(t)
#             # 确保左子树的标签小于右子树的标签 (结构要求)
#             if label(left) >= label(right):
#                 return False
#             # 递归检查左子树和右子树，并更新各自的范围
#             return (is_bst_helper(left, min_val, label(t)) and
#                     is_bst_helper(right, label(t), max_val))
#         else:
#             # BST最多有两个分支
#             return False
#
#     # 初始调用，范围是负无穷到正无穷
#     return is_bst_helper(t, float('-inf'), float('inf'))

# 你的代码中对单分支和双分支的假设比较强，
# 优化后的版本也继承了这一点。
# 一个更标准的BST实现会有 t.left 和 t.right 属性，使得结构更清晰。

def prune_small(t, n):
    """Prune the tree mutatively, keeping only the n branches
    of each node with the smallest labels.

    >>> t1 = Tree(6)
    >>> prune_small(t1, 2)
    >>> t1
    Tree(6)
    >>> t2 = Tree(6, [Tree(3), Tree(4)])
    >>> prune_small(t2, 1)
    >>> t2
    Tree(6, [Tree(3)])
    >>> t3 = Tree(6, [Tree(1), Tree(3, [Tree(1), Tree(2), Tree(3)]), Tree(5, [Tree(3), Tree(4)])])
    >>> prune_small(t3, 2)
    >>> t3
    Tree(6, [Tree(1), Tree(3, [Tree(1), Tree(2)])])
    """
    while len(t.branches) > n:
        largest = max (t.branches, key=lambda x : x.label)
        t.branches.remove(largest)
        #用remove,删除指定对象，而不是索引对应的，而且恰好只删除一个，符合题意
    for b in t.branches:
        prune_small(b, n)

def sum_rec(s, k):
    """Return the sum of the first k elements in s.

    >>> a = Link(1, Link(6, Link(8)))
    >>> sum_rec(a, 2)
    7
    >>> sum_rec(a, 5)
    15
    >>> sum_rec(Link.empty, 1)
    0
    """
    # Use a recursive call to sum_rec; don't call sum_iter
    if k == 0 or s is Link.empty:
        return 0
    else:
        return s.first + sum_rec(s.rest, k - 1)


def sum_iter(s, k):
    """Return the sum of the first k elements in s.

    >>> a = Link(1, Link(6, Link(8)))
    >>> sum_iter(a, 2)
    7
    >>> sum_iter(a, 5)
    15
    >>> sum_iter(Link.empty, 1)
    0
    """
    # Don't call sum_rec or sum_iter
    sum = 0
    tmp = s
    while k > 0 and tmp is not Link.empty:
        sum += tmp.first
        tmp = tmp.rest
        k -= 1
    return sum

def overlap(s, t):
    """For increasing s and t, count the numbers that appear in both.

    >>> a = Link(3, Link(4, Link(6, Link(7, Link(9, Link(10))))))
    >>> b = Link(1, Link(3, Link(5, Link(7, Link(8)))))
    >>> overlap(a, b)  # 3 and 7
    2
    >>> overlap(a.rest, b)  # just 7
    1
    >>> overlap(Link(0, a), Link(0, b))
    3
    """
    if s is Link.empty or t is Link.empty:
        return 0
    if s.first == t.first:
        return 1 + overlap(s.rest, t.rest)
    if s.first < t.first:
        return  overlap(s.rest, t)
    else :
        return  overlap(s, t.rest)

def duplicate_link(s, val):
    """Mutates s so that each element equal to val is followed by another val.

    >>> x = Link(5, Link(4, Link(5)))
    >>> duplicate_link(x, 5)
    >>> x
    Link(5, Link(5, Link(4, Link(5, Link(5)))))
    >>> y = Link(2, Link(4, Link(6, Link(8))))
    >>> duplicate_link(y, 10)
    >>> y
    Link(2, Link(4, Link(6, Link(8))))
    >>> z = Link(1, Link(2, Link(2, Link(3))))
    >>> duplicate_link(z, 2) # ensures that back to back links with val are both duplicated
    >>> z
    Link(1, Link(2, Link(2, Link(2, Link(2, Link(3))))))
    """
    tmp = s
    while tmp is not Link.empty:
        if tmp.first == val:
            new_node = Link(val, tmp.rest)
            tmp.rest = new_node
            tmp = new_node.rest
        else:
            tmp = tmp.rest

def display(s, k=10):
    """Print the first k digits of infinite linked list s as a decimal.

    >>> s = Link(0, Link(8, Link(3)))
    >>> s.rest.rest.rest = s.rest.rest
    >>> display(s)
    0.8333333333...
    """
    assert s.first == 0, f'{s.first} is not 0'
    digits = f'{s.first}.'
    s = s.rest
    for _ in range(k):
        assert s.first >= 0 and s.first < 10, f'{s.first} is not a digit'
        digits += str(s.first)
        s = s.rest
    print(digits + '...')

def divide(n, d):
    """Return a linked list with a cycle containing the digits of n/d.

    >>> display(divide(5, 6))
    0.8333333333...
    >>> display(divide(2, 7))
    0.2857142857...
    >>> display(divide(1, 2500))
    0.0004000000...
    >>> display(divide(3, 11))
    0.2727272727...
    >>> display(divide(3, 99))
    0.0303030303...
    >>> display(divide(2, 31), 50)
    0.06451612903225806451612903225806451612903225806451...
    """
    #While constructing the decimal expansion,
    #store the tail for each n in a dictionary keyed by n.
    #When some n appears a second time,
    #instead of constructing a new Link,
    #set its original link as the rest of the previous link.
    #That will form a cycle of the appropriate length.
    assert n > 0 and n < d
    result = Link(0)  # The zero before the decimal point
    dict = {}
    tail = result
    while not n in list(dict):
        q, r = 10 * n // d, 10 * n % d
        tail.rest = Link(q)
        tail = tail.rest
        dict[n] = tail
        n = r
    if n in list(dict):
        tail.rest = dict[n]
    return result




# Tree Data Abstraction

class Tree:
    def __init__(self, label, branches=[]):
        self.label = label
        for branch in branches:
            assert isinstance(branch, Tree)
        self.branches = list(branches)

    def is_leaf(self):
        return not self.branches

    def __repr__(self):
        if self.is_leaf():
            return f'Tree({self.label})'
        else:
            # repr(b) 会递归调用每个分支的 __repr__ 方法
            branch_str = ', '.join([repr(b) for b in self.branches])
            return f'Tree({self.label}, [{branch_str}])'

# Link list Data Abstraction
class Link:
    empty = ()
    def __init__(self, first, rest=empty):
        #可以直接声明为empty而不用写成Link.empty,因为它在class Link的作用域里面
        assert rest is Link.empty or isinstance(rest, Link)
        #这里的Link.empty是因为这个是在init方法调用时的局部作用域中执行，故需要通过类属性获得empty
        #isinstance:Return whether an object is an instance of a class or of a subclass thereof
        self.first = first
        self.rest = rest

    def __repr__(self):
        # 基本情况：如果这是链表的最后一个节点
        if self.rest is Link.empty:
            return f'Link({self.first})'
        # 递归情况：如果后面还有节点
        else:
            return f'Link({self.first}, {repr(self.rest)})'