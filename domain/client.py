from builtins import property


class Client:
    """
    This is how we know who a user is. It's pretty much just a data store, but it also
    has a function to call its personal ClientConnection's send method.
    """

    def __init__(self, sendfunc, nick="anonymous", name="anonymous", host="anonymous"):
        self._nick = nick
        self._name = name
        self._host = "qtmost4ever"
        self._channels = []
        self._sendfunc = sendfunc

    @property
    def nick(self):
        """
        This client's nick.

        :rtype: str
        """
        return self._nick

    @property
    def name(self):
        """
        This client's name.

        :rtype: str
        """
        return self._name

    @property
    def host(self):
        """
        This client's host. This is what we should be hiding to cloak users!

        :rtype: str
        """
        return self._host

    @nick.setter
    def nick(self, value):
        self._nick = value

    @name.setter
    def name(self, value):
        self._name = value

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def channels(self):
        """
        The channels this client is in. Each channel needs to have this client in their client list as well!

        :rtype: [Channel, ...]
        """
        return self._channels

    @property
    def identity(self):
        """
        This client's unique identifier.

        :rtype: str
        """
        return "{nick}!~{name}@{host}".format(nick=self._nick, name=self._name, host=self._host)

    @property
    def send(self):
        """
        This points to ClientConnection.send().
        :rtype: function
        """
        return self._sendfunc
