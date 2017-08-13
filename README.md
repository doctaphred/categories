# categories
Set-theoretic "types" for Python

```python

>>> from categories import *

>>> object in anything
True
>>> float('nan') in anything
True

>>> object in (anything | anything)
True
>>> object in (anything & anything)
True
>>> object in (anything ^ anything)
False

>>> nothing = ~anything
>>> object in nothing
False

>>> object in (anything | nothing)
True
>>> object in (anything & nothing)
False
>>> object in (anything ^ nothing)
True

>>> something = ~nothing
>>> object in something
True

>>> ints = Category(isinstance, int)
>>> floats = Category(isinstance, float)
>>> numbers = ints | floats
>>> 1 in ints
True
>>> 1 in floats
False
>>> 1 in numbers
True
>>> 1.0 in ints
False
>>> 1.0 in floats
True
>>> 1.0 in numbers
True
>>> 'a' in ints
False
>>> 'a' in floats
False
>>> 'a' in numbers
False

>>> values < 10
lt(value, 10)
>>> 2 in (values < 10)
True
>>> 2 in (values < 1)
False

>>> 2 in ints & (values < 10)
True
>>> 2.0 in ints & (values < 10)
False
>>> 2.0 in (ints | floats) & (values < 10)
True
>>> 'waddup' in (ints | floats) & (values < 10)
False
>>> 'waddup' in (ints | floats) | (values < 10)
False
>>> 'waddup' in (ints | floats) | (values < 10) | anything
True

>>> sized = has.__len__
>>> containers = has.__contains__
>>> iterables = has.__iter__
>>> iterators = iterables & has('__next__', '__iter__')
>>> generators = iterators & has('send', 'throw', 'close')
>>> indexable = has('__getitem__', 'index')
>>> reversible = has.__reversed__
>>> countable = has.count
>>> sequences = Fold(
...     sized, iterables, containers, indexable, reversible, countable)

>>> [] in sized
True
>>> [] in containers
True
>>> [] in iterables
True
>>> [] in iterators
False
>>> iter([]) in iterators
True
>>> iter([]) in generators
False
>>> (x for x in []) in generators
True
>>> iter([]) in indexable
False
>>> [] in indexable
True
>>> [] in sequences
True
>>> {} in sequences
False
>>> set() in sequences
False

```