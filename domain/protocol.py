"""
Protocol's job is to take function calls and turn them into IRC commands.
In other words, it's here so you don't have to write raw IRC.

Don't write raw IRC anywhere else.

https://tools.ietf.org/html/rfc2812
"""

from builtins import *

from domain.constants import Response


class Protocol:
    @staticmethod
    def privmsg(client, channel, message):
        template = ":{identity} PRIVMSG {channel} :{message}"
        return template.format(identity=client.identity,
                               channel=channel.name,
                               message=message)

    @staticmethod
    def quit(client, reason="Quit"):
        template = ":{identity} QUIT :{reason}"
        return template.format(identity=client.identity,
                               reason=reason)

    @staticmethod
    def part(client, channel, reason="Leaving"):
        template = ":{identity} PART {channel} :{reason}"
        return template.format(identity=client.identity,
                               channel=channel.name,
                               reason=reason)

    @staticmethod
    def join(client, channel):
        template = ":{identity} JOIN {channel}"
        return template.format(identity=client.identity,
                               channel=channel.name)

    @staticmethod
    def pong():
        return 'PONG'

    @staticmethod
    def handshake(client):

        # TODO: This isn't generic at all, needs fix.

        response = [  # Protocol
                      'PING :kek',

                      ":localhost {RPL_WELCOME} {nick} :-- Welcome to qtmost server, {nick}",
                      ":localhost {RPL_YOURHOST} {nick} :-- You're connecting from a host, most likely",
                      ":localhost {RPL_CREATED} {nick} :-- This server was created",
                      ":localhost {RPL_MYINFO} {nick} :-- Your information",

                      # MOTD
                      ":localhost {RPL_MOTDSTART} {nick} :=== Begin super important guide to optimal happiness ===",
                      ":localhost {RPL_MOTD} {nick} :|                                                      |",
                      ":localhost {RPL_MOTD} {nick} :|  Remember to stay qt.                                |",
                      ":localhost {RPL_MOTD} {nick} :|                                                      |",
                      ":localhost {RPL_ENDOFMOTD} {nick} :=== End super important guide to optimal happiness ====="]

        return [line.format(nick=client.nick, **Response.todict()) for line in response]

    # Nick
    class Nick:
        @staticmethod
        def response(oldnick, newnick):
            template = ":{oldnick} NICK {newnick}"
            return template.format(oldnick=oldnick, newnick=newnick)

        @staticmethod
        def announce(client, newnick):
            template = ":{identity} NICK {newnick}"
            return template.format(identity=client.identity, newnick=newnick)

    # Whois
    class Whois:

        # TODO: Find out what these are supposed to be. They might be freenode specific.
        # 671
        # b':cameron.freenode.net 671 yukarin qtfriend :is using a secure connection'
        #
        # 330
        # b':cameron.freenode.net 330 yukarin qtfriend QTFriend :is logged in as'

        @staticmethod
        def whoisuser():
            # RPL_WHOISUSER
            # b':cameron.freenode.net 311 yukarin qtfriend ~qtfriend unaffiliated/qtfriend * :some qt'
            pass

        @staticmethod
        def whoischannels():
            # RPL_WHOISCHANNELS
            # b':cameron.freenode.net 319 yukarin qtfriend :#blah #otherchan '
            pass

        @staticmethod
        def whoisserver():
            # RPL_WHOISSERVER
            # b':cameron.freenode.net 312 yukarin qtfriend sendak.freenode.net :Vilnius, Lithuania, EU'
            pass

        @staticmethod
        def endofwhois():
            # RPL_ENDOFWHOIS
            # b':cameron.freenode.net 318 yukarin qtfriend :End of /WHOIS list.'
            pass
