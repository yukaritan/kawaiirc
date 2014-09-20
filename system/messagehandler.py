from builtins import staticmethod

import re

from util import logger


class MessageHandler:
    """
    This class manages our hooks and it's its responsibility to pick and run the right hook function for each message.
    """

    HOOKS = []

    def __init__(self):
        pass

    @staticmethod
    def addhook(regex, func):
        """
        Associates a function with a regex.

        :type regex: str
        :type func: function
        :rtype: None
        """
        logger.debug("Adding hook for '{regex}'", regex=regex)
        MessageHandler.HOOKS.append((re.compile(regex), func))

    @staticmethod
    def getfunc(data):
        """
        Tries hooks until it finds one that matches. The function and matching data is then returned.

        :type data: str
        :rtype: (regex, function)
        """
        for regex, func in MessageHandler.HOOKS:
            match = regex.match(data)
            if match:
                return func, match

        logger.debug('Failed to handle line: "{data}"', data=data)

        return None, None

    @staticmethod
    def handleline(data, client, channels):
        """
        Given supplied data, this method selects a function to run based on which regex gets a match first.
        Returns a list of IRC friendly strings to send back to the server.

        :type data: str
        :type client: Client
        :type channels: [Channel, ...]
        :rtype: [str, ...]
        """
        # logger.debug("Handling line from {nick}: {data}", nick=client.nick, data=data)
        func, match = MessageHandler.getfunc(data)
        if func is not None:
            return func(data, match.groupdict(), client, channels)