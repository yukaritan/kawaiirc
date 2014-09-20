class TableRow:
    template = ("<tr>"
                "<td>{name}</td>"
                "<td>{params}</td>"
                "<td>{description}</td>"
                "<td>{example}</td>"
                "<td>{returns}</td>"
                "</tr>")

    def __init__(self, name, description=None, example=None, params=None, returns=None):
        """
        :type returns: str
        :type params: [str]
        :type example: str
        :type description: str
        :type name: str
        """
        self.name = name
        self.description = description
        self.example = example
        self.params = params
        self.returns = returns

    def __str__(self):
        return TableRow.template.format(**{k: v or "<font color='#aaaaaa'>n/a</font>" for k, v in self.__dict__.items()})