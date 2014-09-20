from builtins import property

from domain.protocol import Protocol


class Channel:
    """
    This is a channel. Each channel has a list of clients and a method that can send the same thing to every client in a loop.
    It actually has two, and they're very similar to each other. The difference is that send() sends to everyone in the channel, while say() sends to everyone except the client who caused the message to be sent in the first place.
    """

    def __init__(self, name, owner, topic="no topic"):
        """
        :type name: str
        :type topic: str
        :type owner: Client
        """
        self._name = name
        self._owner = owner
        self._topic = topic
        self._clients = []  # list of clients

    @property
    def name(self):
        """
        The name of the channel

        :example: "#aardvark"
        :rtype: str
        """
        return self._name

    @property
    def owner(self):
        """
        The user who created the channel

        :rtype: Client
        """
        return self._owner

    @property
    def topic(self):
        """
        The topic of the channel

        :example: "Aardvarks are awesome"
        :rtype: str
        """
        return self._topic

    @property
    def clients(self):
        """
        A list of clients currently in the channel.
        Each client needs to have this channel in their channel list as well!

        :rtype: [Client, ...]
        """
        return self._clients

    def send(self, data):
        """
        Sends data to everyone in the channel. It can be anything, like a join message.

        :type data: str
        :rtype: None
        """
        for cl in self._clients:
            cl.send(data)

    def say(self, client, message):
        """
        Sends message as a PRIVMSG to everyone in the channel except the person who sent it.

        :type client: Client
        :type message: str
        :rtype: None
        """
        message = Protocol.privmsg(client, self, message)
        for cl in self._clients:
            if cl is not client:
                cl.send(message)