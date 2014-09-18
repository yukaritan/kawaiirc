from builtins import classmethod, AttributeError, getattr, dir


class Dictable:
    """
    Adds a static function to a class which generates and returns  a list
    of all its non-private members and stores them in a dictionary.
    """

    @classmethod
    def todict(cls):
        try:
            return cls._cached_member_dict
        except AttributeError:
            cls._cached_member_dict = {name: getattr(cls, name)
                                       for name in dir(cls)
                                       if not name.startswith('_')}
            return cls._cached_member_dict