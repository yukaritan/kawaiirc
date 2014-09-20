from builtins import str


class Table:
    template = ("<table border='1'>"
                "<tr>"
                "<th>Name</th>"
                "<th>Params</th>"
                "<th>Description</th>"
                "<th>Example</th>"
                "<th>Returns</th>"
                "</tr>"
                "{tablerows}"
                "</table>")

    def __init__(self):
        self.tablerows = []

    def __str__(self):
        return Table.template.format(tablerows='\n'.join(str(tr) for tr in self.tablerows))