test = {
  'name': 'Lists, Sequences, and Mutation WWPD',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> s = [7//3, 5, [4, 0, 1], 2]
          >>> s[0]
          2
          >>> s[2]
          [4, 0, 1]
          >>> s[-1]
          2
          >>> len(s)
          4
          >>> 4 in s
          False
          >>> 4 in s[2]
          True
          >>> s[2] + [3 + 2]
          [4, 0, 1, 5]
          >>> 5 in s[2]
          False
          >>> s[2] * 2
          [4, 0, 1, 4, 0, 1]
          >>> list(range(3, 6))
          [3, 4, 5]
          >>> range(3, 6)
          range(3, 6)
          >>> r = range(3, 6)
          >>> [r[0], r[2]]
          [3, 5]
          >>> range(4)[-1]
          3
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> [2 * x for x in range(4)]
          [0, 2, 4, 6]
          >>> [y for y in [6, 1, 6, 1] if y > 2]
          [6, 6]
          >>> [[1] + s for s in [[4], [5, 6]]]
          [[1, 4], [1, 5, 6]]
          >>> [z + 1 for z in range(10) if z % 3 == 0]
          [1, 4, 7, 10]
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # If nothing would be output by Python, type Nothing
          >>> # If the code would error, type Error
          >>> s = [6, 7, 8]
          >>> print(s.append(6))
          None
          >>> s
          [6, 7, 8, 6]
          >>> s.insert(0, 9)
          >>> s
          [9, 6, 7, 8, 6]
          >>> x = s.pop(1)
          >>> s
          [9, 7, 8, 6]
          >>> s.remove(x)
          >>> s
          [9, 7, 8]
          >>> a, b = s, s[:]
          >>> a is s
          True
          >>> b == s
          True
          >>> b is s
          False
          >>> a.pop()
          8
          >>> a + b
          [9, 7, 9, 7, 8]
          >>> s = [3]
          >>> s.extend([4, 5])
          >>> s
          [3, 4, 5]
          >>> a
          [9, 7]
          >>> s.extend([s.append(9), s.append(10)])
          >>> s
          [3, 4, 5, 9, 10, None, None]
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': False,
      'type': 'wwpp'
    }
  ]
}
