from builtins import *
import os
from domain.channel import Channel
from domain.client import Client
from domain.protocol import Protocol
from system.ircfactory import IRCFactory

from system.messagehandler import MessageHandler
from table import Table
from tablerow import TableRow
from util.dictable import Dictable


class Autodoc:
    """
    Okay, so writing documentation is tedious and boring. Tedious and boring things can be automated.
    This is my attempt at doing so.
    """

    def __init__(self):
        pass

    @staticmethod
    def getvariables(cls):
        """
        Gets all variables in a class, returns them in a list.
        Static method.

        :example: getvariables(Autodoc)
        :type cls: object | Class
        :rtype: [variable: object, ...]
        """
        return [(name, getattr(cls, name)) for name in dir(cls)
                if not name.startswith('_')
                and not callable(getattr(cls, name))]

    @staticmethod
    def getmethods(cls):
        """
        Gets all methods in a class, returns them in a list.
        Static method.

        :example: getmethods(Autodoc)
        :type cls: object | Class
        :rtype: [method: function, ...]
        """
        return [(name, getattr(cls, name)) for name in dir(cls)
                if not name.startswith('_')
                and callable(getattr(cls, name))]

    @staticmethod
    def slicedocstring(obj):
        """
        Splits an object's docstring into a list of stripped lines.

        :type obj: object
        :rtype: [str, ...]
        """
        if obj.__doc__ is None:
            return []

        return [line.strip().replace('<', '&lt;').replace('>', '&gt;')
                for line in obj.__doc__.splitlines()
                if line.strip()]

    @staticmethod
    def itemtotablerow(name, item):
        """
        Takes an item returned from getmethod or getvariables and returns a TableRow

        :type name: str
        :type item: object
        :rtype: tablerow.TableRow
        """
        tablerow = TableRow(name)
        docstr = Autodoc.slicedocstring(item)

        tablerow.description = '<br>\n'.join(s for s in docstr if not s.startswith(':'))
        tablerow.example = Autodoc.getdocstrbytype(':example:', docstr)
        tablerow.returns = Autodoc.getdocstrbytype(':rtype:', docstr)
        tablerow.params = ',<br>\n'.join(s.split(' ', 1)[1].replace('<', '&lt;').replace('>', '&gt;')
                                         for s in docstr if s.startswith(':type '))

        return tablerow

    @staticmethod
    def getdocstrbytype(startswith, docstr):
        """
        Returns a string where all the lines starting with startswith joined by ",<br>\\n"

        :type startswith: str
        :rtype: str
        """
        return ',<br>\n'.join(s.split(': ', 1)[1].replace('<', '&lt;').replace('>', '&gt;')
                              for s in docstr if s.startswith(startswith))

    @staticmethod
    def itemrowstotable(nameitems):
        """
        Takes the names and items returned by getmethod or getvariables and returns a table.

        :type nameitems: [(str, object), ...]
        :rtype: table.Table
        """
        table = Table()

        for name, item in nameitems:
            tr = Autodoc.itemtotablerow(name, item)
            table.tablerows.append(tr)

        return table


def test():
    import sys

    classes = [Channel,
               Client,
               IRCFactory,
               MessageHandler,
               Autodoc,
               Dictable,
               Protocol,
               Protocol.Nick,
               Protocol.Whois]

    # os.mkdir("docs")

    for cls in classes:
        _stdout = sys.stdout
        path = 'docs/{name}.htm'.format(name=cls.__name__.lower())
        with open(path, 'w+') as sys.stdout:

            print("<!doctype html>")
            print("<html>")

            print("<head>")
            print("<title>Autodoc: {name}</title>".format(name=cls.__name__))
            print("""<style>body {font-family: Arial;}</style>""")
            print("</head>")

            print("<body>")

            print('<h1>{name}</h1>'.format(name=cls.__name__))
            print('<p>{desc}</p>'.format(desc='<br>\n'.join(Autodoc.slicedocstring(cls))))
            print()
            print('<h2>Variables</h2>')
            print(Autodoc.itemrowstotable(Autodoc.getvariables(cls)))
            print()
            print('<h2>Methods</h2>')
            print(Autodoc.itemrowstotable(Autodoc.getmethods(cls)))

            print("<br><hr><h5>Generated with Autodoc</h5>")

            print("</body>")
            print("</html>")

        sys.stdout = _stdout


if __name__ == '__main__':
    test()