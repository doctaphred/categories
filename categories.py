import operator
from itertools import chain


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


@object.__new__
class has:

    def __getattr__(self, name):
        return Category(hasattr, name)

    def __call__(self, *names, fold=all):
        return Fold(*(Category(hasattr, name) for name in names), fold=fold)


@object.__new__
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
