
class Node:

    def __init__(self, symbol, pos, gap, predecessor=None) -> None:

        # Input parameters
        self._symbol = symbol
        self._pos = pos
        self._gap = gap
        self._predecessor = predecessor

        # Other params
        self._parents = []
        self._path = 0

    @property
    def symbol(self):
        return self._symbol
    
    @property
    def pos(self):
        return self._pos

    @property
    def gap(self):
        return self._gap
    
    @property
    def predecessor(self):
        return self._predecessor

    @property
    def path(self):
        return self._path

    @property
    def parents(self):
        return self._parents

    @parents.setter
    def parents(self, parent):
        """
        Add a parent node.
        """
        self._parents.append(parent)

    @path.setter
    def path(self, path):
        """
        Update number of paths to the node.
        """
        self._path = path

    def __repr__(self) -> str:
        return f'Node {self._pos}: {self._symbol}'
