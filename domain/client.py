"""
This is how we know who a user is. It's pretty much just a data store, but it also
has a function to call its personal ClientConnection's send method.
"""

from builtins import property


class Client:
    def __init__(self, nick="anonymous", name="anonymous", host="anonymous", sendfunc=None):
        self._nick = nick
        self._name = name

        self._host = "qtmost4ever"  # This is what we should be hiding to cloak users!

        self._mode = ''
        self._channels = []  # List of channels. Each channel needs to have this client in their clients list as well
        self._sendfunc = sendfunc  # This points to ClientConnection.send().

    @property
    def nick(self):
        return self._nick

    @property
    def name(self):
        return self._name

    @property
    def host(self):
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
        return self._channels

    @property
    def mode(self):
        return self._mode

    @property
    def identity(self):
        return "{nick}!~{name}@{host}".format(nick=self._nick, name=self._name, host=self._host)

    @property
    def send(self):
        # This points to ClientConnection.send().
        return self._sendfunc

    @mode.setter
    def mode(self, value):
        self._mode = value