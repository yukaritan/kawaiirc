"""
This is where networking is born! It's also where we list all our clients and channels.
When a user connects, a ClientConnection is born to cater to them.
"""

from builtins import super, property, dict
from collections import deque
from twisted.internet.protocol import ServerFactory


class IRCFactory(ServerFactory):
    def __init__(self, *args, **kw):
        super(*args, **kw)
        self._clients = deque()
        self._channels = dict()

    @property
    def clients(self):
        """
        :rtype : deque
        """
        return self._clients

    @clients.setter
    def clients(self, value):
        """
        :type value: deque
        """
        self._clients = value

    @property
    def channels(self):
        """
        :rtype : dict
        """
        return self._channels
