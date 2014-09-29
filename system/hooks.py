"""
Everything is a hook. Everything sent from a client will either be caught
by a hook and handled, or it's not caught, and ends up in a log somewhere.

Hooks consist of two things. A regex, and a function.
A regex is a regular string, and may look like this:
'^USER (?P<user>[^\s]+) (?P<mode>[^\s]+) (?P<junk>[^\s]+) :(?P<name>.*)'

You'll find the function below, it's called handle_user(...).

Every hook function is expected to take four parameters:
    data: Data is the original string that triggered the hook to begin with.
    match: This is a dictionary. The regex above would yield the following dict:
           {'user': 'user@blah.balh',
            'mode': '+i',
            'junk': 'some-junk-here',
            'name': 'some name here'}
    client: This is the client that triggered the hook.
    channels: This is a list of all the channels on the server.

"""

from builtins import set
from itertools import chain

from domain.channel import Channel
from domain.client import Client
from domain.protocol import Protocol
from util import logger


def handle_user(data, match, client, channels):
    """
    This is a handshake. We'll blatantly disregard the whole pinging thing,
    because I don't really care. Clients still ping the server as it is.
    We'll see how it works out.

    '^USER (?P<user>[^\s]+) (?P<mode>[^\s]+) (?P<junk>[^\s]+) :(?P<name>.*)'

    :type data: str
    :type match: dict
    :type client: Client
    :type channels: list
    """
    client.name = match['name']
    client.host = match['host']
    logger.info("Set new user's name to '{name}'", name=client.name)
    logger.info("Set new user's host to '{host}'", host=client.host)

    response = Protocol.handshake(client)

    return [line.format(nick=client.nick) for line in response]


def handle_nick(data, match, client, channels):
    """
    When a user changes their nick, tell everyone in all the channels they're in
    about it.

    '^NICK (?P<nick>.*)'

    :type data: str
    :type match: dict
    :type client: Client
    :type channels: list
    """

    newnick = match['nick']

    logger.info("Set new user's nick to '{newnick}'", newnick=newnick)

    client.send(Protocol.Nick.response(client.nick, newnick))

    announce = Protocol.Nick.announce(client, newnick)
    for cl in set(chain.from_iterable(chan.clients for chan in client.channels)):
        if cl is not client:
            cl.send(announce)

    client.nick = newnick


def handle_ping(data, match, client, channels):
    """
    Ping! Send pong back.

    '^PING.*'

    :type data: str
    :type match: dict
    :type client: Client
    :type channels: list
    """
    # logger.debug("Got ping from {nick}", nick=client.nick)
    return [Protocol.pong()]


def handle_pong(data, match, client, channels):
    """
    Pong! This will probably never happen because the server isn't pinging.

    '^PONG.*'

    :type data: str
    :type match: dict
    :type client: Client
    :type channels: list
    """
    # logger.debug("Got pong from {nick}", nick=client.nick)


def handle_join(data, match, client, channels):
    """
    Someone joined a channel! A few things can happen now.
    Either they joined a channel that doesn't exist, and in that case, we create it and
    set them as the owner.
    If it already exists, let's announce their arrival to the participants.

    '^JOIN (?P<channels>.*)'

    :type data: str
    :type match: dict
    :type client: Client
    :type channels: list
    """

    templates = [":{identity} JOIN {channel}",  # join
                 ":{server} 332 {nick} {channel} :{topic}",  # topic
                 ":{server} 353 {nick} = {channel} :{nicks}",  # names in channel
                 ":{server} 366 {nick} {channel} :End of /NAMES list."]  # end of names

    for channame in match['channels'].split(','):
        channame = channame.strip()
        logger.debug("{nick} joins channel {channame}", nick=client.nick, channame=channame)

        if channame not in channels:
            channels[channame] = Channel(name=channame, owner=client)

        channel = channels[channame]
        channel.clients.append(client)
        client.channels.append(channel)

        nicks = ' '.join(client.nick for client in channel.clients)
        client.send([template.format(channel=channel.name,
                                     identity=client.identity,
                                     nick=client.nick,
                                     nicks=nicks,
                                     server="localhost",
                                     topic=channel.topic)
                     for template in templates])

        announce = Protocol.join(client, channel)
        channel.send(announce)


def handle_part(data, match, client, channels):
    """
    Someone is leaving a channel. Let's tell everyone about it and
    remove them from the channel's user listing (and the channel from the client's).

    '^PART (?P<channel>[^\s]+)( :(?P<message>.*))'

    :type data: str
    :type match: dict
    :type client: Client
    :type channels: list
    """

    channame = match['channel']

    logger.debug("{nick} leaves channel {channame}", nick=client.nick, channame=channame)

    if not channame in channels:
        logger.warn("no channel named {channame}", channame=channame)
        return

    channel = channels[channame]

    client.channels.remove(channel)
    channels[channame].clients.remove(client)

    announce = Protocol.part(client, channel, match['message'] or 'leaving')
    channel.send(announce)


def handle_privmsg(data, match, client, channels):
    """
    This happens when someone sends something. If the targeted channel exists,
    send it to everyone in it.

    TODO: Users can be privmsg'd too, so we should be able to handle that.

    '^PRIVMSG (?P<channel>[^\s]+) :(?P<message>.*)'

    :type data: str
    :type match: dict
    :type client: Client
    :type channels: list
    """

    logger.debug('{nick} says "{message}" to {channel}', nick=client.nick, **match)
    channame = match['channel']

    if channame in channels:
        channels[channame].say(client, match['message'])
    else:
        logger.warn('channel {channame} does not exist', channame=channame)


def handle_mode(data, match, client, channels):
    """
    Someone is setting their mode. I don't know enough about this to talk about it yet.

    '^MODE (?P<nick>[^\s]+) (?P<mode>.*)'

    :type data: str
    :type match: dict
    :type client: Client
    :type channels: list
    """

    logger.debug("setting {nick}'s mode to {mode}, as per their request", **match)
    client.mode = match['mode'].replace('+', '')


def handle_whois(data, match, client, channels):
    """
    Someone is asking who someone is. Let's tell them what we know!
    TODO: All of it.

    '^WHOIS (?P<nick>[^\s]+)'

    :type data: str
    :type match: dict
    :type client: Client
    :type channels: list
    """

    response = [Protocol.Whois.whoisuser(),
                Protocol.Whois.whoischannels(),
                Protocol.Whois.whoisserver(),
                Protocol.Whois.endofwhois()]

    """
    3.6.2 Whois query

          Command: WHOIS
       Parameters: [ <target> ] <mask> *( "," <mask> )

       This command is used to query information about particular user.
       The server will answer this command with several numeric messages
       indicating different statuses of each user which matches the mask (if
       you are entitled to see them).  If no wildcard is present in the
       <mask>, any information about that nick which you are allowed to see
       is presented.

       If the <target> parameter is specified, it sends the query to a
       specific server.  It is useful if you want to know how long the user
       in question has been idle as only local server (i.e., the server the
       user is directly connected to) knows that information, while
       everything else is globally known.

       Wildcards are allowed in the <target> parameter.

       Numeric Replies:

               ERR_NOSUCHSERVER              ERR_NONICKNAMEGIVEN
               RPL_WHOISUSER                 RPL_WHOISCHANNELS
               RPL_WHOISCHANNELS             RPL_WHOISSERVER
               RPL_AWAY                      RPL_WHOISOPERATOR
               RPL_WHOISIDLE                 ERR_NOSUCHNICK
               RPL_ENDOFWHOIS

       Examples:

       WHOIS wiz                       ; return available user information
                                       about nick WiZ

       WHOIS eff.org trillian          ; ask server eff.org for user
                                       information  about trillian
    """