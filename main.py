from twisted.internet import reactor

from system.clientconnection import ClientConnection
from system.hooks import handle_user, handle_nick, handle_ping, handle_pong, handle_join, handle_part, \
    handle_privmsg, handle_mode
from system.ircfactory import IRCFactory
from system.messagehandler import MessageHandler
from util import logger

logger.debugmode = True


def addhooks():
    """
    This is a temporary solution for hooking regexes up to various functions.
    It'll look pretty much like this in the future too, but it won't be right here,
    and it'll be built in such a way that you can easily make plugins.
    """

    MessageHandler.addhook('^PRIVMSG (?P<channel>[^\s]+) :(?P<message>.*)', handle_privmsg)

    MessageHandler.addhook('^PING.*', handle_ping)
    MessageHandler.addhook('^PONG.*', handle_pong)

    MessageHandler.addhook('^NICK (?P<nick>.*)',
                           handle_nick)

    MessageHandler.addhook('^USER (?P<user>[^\s]+)'
                           ' (?P<mode>[^\s]+)'
                           ' (?P<host>[^\s]+)'
                           ' :(?P<name>.*)',
                           handle_user)

    MessageHandler.addhook('^JOIN (?P<channels>.*)', handle_join)
    MessageHandler.addhook('^PART (?P<channel>[^\s]+)( :(?P<message>.*))?', handle_part)

    MessageHandler.addhook('^MODE (?P<nick>[^\s]+) (?P<mode>.*)', handle_mode)


def main():
    logger.info("Adding hooks...")
    addhooks()
    logger.info("Done with hooks!")

    logger.info("Setting up factory")
    factory = IRCFactory()
    factory.protocol = ClientConnection

    logger.info("Listening")
    reactor.listenTCP(6667, factory)
    reactor.run()


if __name__ == '__main__':
    main()