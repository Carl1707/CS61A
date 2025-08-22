def has_path(t, target):
	"""Return whether there is a path in a Tree where the entries along the path
	spell out a particular target.

	>>> greetings = Tree('h', [Tree('i'),
	...                        Tree('e', [Tree('l', [Tree('l', [Tree('o')])]),
	...                                   Tree('y')])])
	>>> print(greetings)
	h
	  i
	  e
		l
		  l
			o
		y
	>>> has_path(greetings, 'h')
	True
	>>> has_path(greetings, 'i')
	False
	>>> has_path(greetings, 'hi')
	True
	>>> has_path(greetings, 'hello')
	True
	>>> has_path(greetings, 'hey')
	True
	>>> has_path(greetings, 'bye')
	False
	>>> has_path(greetings, 'hint')
	False
	"""
	assert len(target) > 0, 'no path for empty target.'
	if t.label == target[0]:
		if  len(target) == 1:
			return True
		else:
			return any([has_path(b,target[1:]) for b in t.branches])
	else:
		return False


def long_paths(tree, n):
	"""Return a list of all paths in tree with length at least n.
	>>> t = Tree(3, [Tree(4), Tree(4), Tree(5)])
	>>> left = Tree(1, [Tree(2), t])
	>>> mid = Tree(6, [Tree(7, [Tree(8)]), Tree(9)])
	>>> right = Tree(11, [Tree(12, [Tree(13, [Tree(14)])])])
	>>> whole = Tree(0, [left, Tree(13), mid, right])
	>>> for path in long_paths(whole, 2):
	...     print(path)
	...
	<0 1 2>
	<0 1 3 4>
	<0 1 3 4>
	<0 1 3 5>
	<0 6 7 8>
	<0 6 9>
	<0 11 12 13 14>
	>>> for path in long_paths(whole, 3):
	...     print(path)
	...
	<0 1 3 4>
	<0 1 3 4>
	<0 1 3 5>
	<0 6 7 8>
	<0 11 12 13 14>
	>>> long_paths(whole, 4)
	[Link(0, Link(11, Link(12, Link(13, Link(14)))))]
	"""
	# 关键在于不要在循环内部直接return。你应该：
	# 在函数（或递归调用的每次执行）的开始处创建一个空的列表paths = []。
	# 在循环中，对每个子分支进行递归调用。
	# 将递归调用的结果（它本身也是一个列表）进行处理，
	# 然后将处理后的新路径 ** 添加（append） ** 到paths列表中。
	# 在函数的最后，也就是循环结束之后，return paths。
	if tree.is_leaf():
		return [Link(tree.label)] if 0 >= n else []
	paths = []
	#在更深递归处定义的paths不会覆写之前的paths
	for b in tree.branches:
		for sub_path in long_paths(b, n - 1):
			paths.append(Link(tree.label, sub_path))
	return paths
	#思路是什么呢：我们知道这个调用返回的是列表，但是我们又不想在创建Link时rest是列表
	#所以我们使用for来遍历，消除了列表，对象都是Link,从而可以连接现在的tree.label
	#之后将这些新的连接加到列表里面，进行返回，从而实现返回列表


def without(s, i):
	"""Return a new linked list like s but without the element at index i.

	>>> s = Link(3, Link(5, Link(7, Link(9))))
	>>> without(s, 0)
	Link(5, Link(7, Link(9)))
	>>> without(s, 2)
	Link(3, Link(5, Link(9)))
	>>> without(s, 4)           # There is no index 4, so all of s is retained.
	Link(3, Link(5, Link(7, Link(9))))
	>>> without(s, 4) is not s  # Make sure a copy is created
	True
	"""
	if s is Link.empty:
		return s
	if i == 0:
		return s.rest
	else:
		return Link(s.first, without(s.rest, i - 1))


def slice_link(link, start, end):
	"""Slices a linked list from start to end (as with a normal Python list).

	>>> link = Link(3, Link(1, Link(4, Link(1, Link(5, Link(9))))))
	>>> new = slice_link(link, 1, 4)
	>>> print(new)
	<1 4 1>
	"""
	pointer = 0
	tmp = link
	while pointer < start:
		tmp = tmp.rest
		pointer += 1
	new_link = tmp
	tmp = new_link
	while pointer < end - 1:
		tmp = tmp.rest
		pointer += 1
	tmp.rest = Link.empty
	return new_link



def level_mutation_link(t, funcs):
	"""Mutates t using the functions in the linked list funcs.

	>>> t = Tree(1, [Tree(2, [Tree(3)])])
	>>> funcs = Link(lambda x: x + 1, Link(lambda y: y * 5, Link(lambda z: z ** 2)))
	>>> level_mutation_link(t, funcs)
	>>> t    # At level 0, apply x + 1; at level 1, apply y * 5; at level 2 (leaf), apply z ** 2
	Tree(2, [Tree(10, [Tree(9)])])
	>>> t2 = Tree(1, [Tree(2), Tree(3, [Tree(4)])])
	>>> level_mutation_link(t2, funcs)
	>>> t2    # Level 0: 1+1=2; Level 1: 2*5=10 => 10**2 = 100, 3*5=15; Level 2 (leaf): 4**2=16
	Tree(2, [Tree(100), Tree(15, [Tree(16)])])
	>>> t3 = Tree(1, [Tree(2)])
	>>> level_mutation_link(t3, funcs)
	>>> t3    # Level 0: 1+1=2; Level 1: 2*5=10; no further levels, so apply remaining z ** 2: 10**2=100
	Tree(2, [Tree(100)])
	"""
	if funcs is Link.empty:
		return
	t.label = funcs.first(t.label)
	remaining = funcs.rest
	if t.is_leaf():
		while remaining is not Link.empty:
			t.label = remaining.first(t.label)
			remaining = remaining.rest
	for b in t.branches:
		level_mutation_link(b, funcs.rest)


class Tree:
	"""A tree has a label and a list of branches.

	>>> t = Tree(3, [Tree(2, [Tree(5)]), Tree(4)])
	>>> t.label
	3
	>>> t.branches[0].label
	2
	>>> t.branches[1].is_leaf()
	True
	"""
	def __init__(self, label, branches=[]):
		self.label = label
		for branch in branches:
			assert isinstance(branch, Tree)
		self.branches = list(branches)

	def is_leaf(self):
		return not self.branches

	def __repr__(self):
		if self.branches:
			branch_str = ', ' + repr(self.branches)
		else:
			branch_str = ''
		return 'Tree({0}{1})'.format(repr(self.label), branch_str)

	def __str__(self):
		return '\n'.join(self.indented())

	def indented(self):
		lines = []
		for b in self.branches:
			for line in b.indented():
				lines.append('  ' + line)
		return [str(self.label)] + lines


class Link:
	"""A linked list.

	>>> s = Link(1)
	>>> s.first
	1
	>>> s.rest is Link.empty
	True
	>>> s = Link(2, Link(3, Link(4)))
	>>> s.first = 5
	>>> s.rest.first = 6
	>>> s.rest.rest = Link.empty
	>>> s                                    # Displays the contents of repr(s)
	Link(5, Link(6))
	>>> s.rest = Link(7, Link(Link(8, Link(9))))
	>>> s
	Link(5, Link(7, Link(Link(8, Link(9)))))
	>>> print(s)                             # Prints str(s)
	<5 7 <8 9>>
	"""
	empty = ()

	def __init__(self, first, rest=empty):
		assert rest is Link.empty or isinstance(rest, Link)
		self.first = first
		self.rest = rest

	def __repr__(self):
		if self.rest is not Link.empty:
			rest_repr = ', ' + repr(self.rest)
		else:
			rest_repr = ''
		return 'Link(' + repr(self.first) + rest_repr + ')'

	def __str__(self):
		string = '<'
		while self.rest is not Link.empty:
			string += str(self.first) + ' '
			self = self.rest
		return string + str(self.first) + '>'

from reprlib import recursive_repr
Link.__repr__ = recursive_repr()(Link.__repr__)

