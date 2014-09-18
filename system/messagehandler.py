"""
This class manages our hooks and it's its responsibility to pick
and run the right hook function for each message.
"""

from builtins import staticmethod

import re

from util import logger


class MessageHandler:
    HOOKS = []

    def __init__(self):
        pass

    @staticmethod
    def addhook(regex, func):
        """
        :type regex: str
        :rtype: None
        """
        logger.debug("Adding hook for '{regex}'", regex=regex)
        MessageHandler.HOOKS.append((re.compile(regex), func))

    @staticmethod
    def getfunc(data):
        """
        Tries hooks until it finds one that matches. The function and matching data is then returned.

        :type data: str
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
        :type data: str
        :type client: Client
        :type channels: list
        :rtype: list
        """
        # logger.debug("Handling line from {nick}: {data}", nick=client.nick, data=data)
        func, match = MessageHandler.getfunc(data)
        if func is not None:
            return func(data, match.groupdict(), client, channels)