from builtins import classmethod, AttributeError, getattr, dir


class Dictable:
    """
    Adds a static function to a class which generates and returns a list of all its non-private members and stores them in a dictionary.
    This should only be used for classes with static content, as the dictionary is generated only once.
    """

    @classmethod
    def todict(cls):
        """
        Returns a list of all of class cls' private members and caches them in a dict.

        :type cls: Class
        :rtype: dict
        """
        try:
            return cls._cached_member_dict
        except AttributeError:
            cls._cached_member_dict = {name: getattr(cls, name)
                                       for name in dir(cls)
                                       if not name.startswith('_')}
            return cls._cached_member_dict