"""
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
"""
import operator
from itertools import chain


def magic(cls):
    return cls()


def not_any(x):
    """
    >>> not_any([])
    True
    >>> not_any([True])
    False
    >>> not_any([False])
    True
    >>> not_any([True, False])
    False
    """
    return not any(x)


def not_all(x):
    """
    >>> not_all([])
    False
    >>> not_all([True])
    False
    >>> not_all([False])
    True
    >>> not_all([True, False])
    True
    """
    return not all(x)


class Category:

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __contains__(self, value):
        try:
            result = self.func(value, *self.args, **self.kwargs)
        except Exception:
            return False
        if result is NotImplemented:
            return False
        return result

    def __and__(self, other):
        return Fold(self, other, fold=all)

    def __or__(self, other):
        return Fold(self, other, fold=any)

    def __xor__(self, other):
        return Fold(self, other, fold=not_all)

    def __invert__(self):
        return Fold(self, fold=not_any)

    def __repr__(self):
        try:
            func_name = self.func.__name__
        except AttributeError:
            func_name = self.func

        args_strs = [str(arg) for arg in self.args]
        kwargs_strs = ['{}={}'.format(k, v) for k, v in self.kwargs.items()]
        args_str = ', '.join(args_strs + kwargs_strs)

        if args_str:
            return '{}(value, {})'.format(func_name, args_str)
        else:
            return '{}(value)'.format(func_name)


class Fold(Category):

    def __init__(self, *subcategories, fold=all):
        self.subcategories = subcategories
        self.fold = fold
        # Flatten subcategories if possible
        try:
            if (len(subcategories) > 1 and
                    all(sub.fold == fold for sub in subcategories)):
                self.subcategories = Fold(*chain.from_iterable(subcategories))
        except AttributeError:
            pass

    def __iter__(self):
        return iter(self.categories)

    def __contains__(self, value):
        return self.fold(value in subcat for subcat in self.subcategories)

    def __repr__(self):
        cat_strs = [str(c) for c in self.subcategories]
        return '{}({{{}}})'.format(self.fold.__name__, ', '.join(cat_strs))


anything = Fold()


@magic
class has:

    def __getattr__(self, name):
        return Category(hasattr, name)

    def __call__(self, *names):
        return Fold(*(Category(hasattr, name) for name in names))


@magic
class values:

    def __eq__(self, obj):
        return Category(operator.eq, obj)

    def __ne__(self, obj):
        return Category(operator.ne, obj)

    def __lt__(self, obj):
        return Category(operator.lt, obj)

    def __gt__(self, obj):
        return Category(operator.gt, obj)

    def __le__(self, obj):
        return Category(operator.le, obj)

    def __ge__(self, obj):
        return Category(operator.ge, obj)
