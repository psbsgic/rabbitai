# pylint: disable=invalid-name


class Row(object):
    def __init__(self, values):
        self.values = values

    def __name__(self):  # pylint: disable=no-self-use
        return "Row"

    def __iter__(self):
        return (item for item in self.values)
