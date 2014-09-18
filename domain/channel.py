"""
This is a channel. Each channel has a list of clients and a method that
can send the same thing to every client in a loop. It actually has two,
and they're very similar to each other. The difference is that send()
sends to everyone in the channel, while say() sends to everyone except
the client who caused the message to be sent in the first place.
"""

from builtins import property

from domain.protocol import Protocol


class Channel:
    def __init__(self, name=None, owner=None, topic="no topic"):
        """
        :type topic: str
        :type owner: Client
        """
        self._name = name
        self._owner = owner
        self._topic = topic
        self._ops = []
        self._clients = []  # list of clients. each client needs to have this channel in their channels list as well

    @property
    def name(self):
        return self._name

    @property
    def owner(self):
        return self._owner

    @property
    def topic(self):
        return self._topic

    @property
    def clients(self):
        return self._clients

    def send(self, message):
        """
        :type message: str
        """
        for cl in self._clients:
            cl.send(message)

    def say(self, client, message):
        """
        :type client: Client
        :type message: str
        """
        message = Protocol.privmsg(client, self, message)
        for cl in self._clients:
            if cl is not client:
                cl.send(message)