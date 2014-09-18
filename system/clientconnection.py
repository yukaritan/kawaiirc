"""
This class talks to clients, runs their messages through our hooks
(by passing them to MessageHandler.handleline(...)) and returns
responses, usually through the send method it shares with its client.
"""

from twisted.protocols import basic

from domain.client import Client
from system.messagehandler import MessageHandler
from domain.protocol import Protocol
from util import logger


class ClientConnection(basic.LineReceiver):
    def __init__(self):
        self._client = Client(sendfunc=self.send)

    def connectionMade(self):
        logger.info("Got new client!")
        self.factory.clients.append(self)

    # noinspection PyMethodOverriding
    def connectionLost(self, reason):
        logger.info('Lost client "{nick}"', nick=self._client.nick)
        announce = Protocol.quit(self._client, "Connection lost")

        for channel in self._client.channels:
            channel.clients.remove(self._client)
            channel.send(announce)

        self.factory.clients.remove(self)

    def lineReceived(self, data):
        """
        :type data: bytes
        """
        data = data.decode()

        # logger.debug('Recieved "{data}" from {nick}',
        #              nick=self._client.nick,
        #              data=data)

        response = MessageHandler.handleline(data, self._client, self.factory.channels)
        if response:
            for data in response:
                self.send(data)

    def send(self, data):
        """
        :type data: str
        """

        # logger.debug('Sending "{data}" to {nick}',
        #              nick=self._client.nick,
        #              data=data)

        self.transport.write((data + '\r\n').encode())
