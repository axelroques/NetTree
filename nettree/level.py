
class Level:

    def __init__(self) -> None:

        self._nodes = []
        self._head = None
        self._start = []
        self._tail = None

    def add_node(self, node):
        """
        Add a node to the level.
        """
        self._nodes.append(node)

    @property
    def nodes(self):
        """
        Get all nodes in the level.
        """
        return self._nodes

    @property
    def head(self):
        """
        Get the "head" node for the level.
        """
        return self._head

    @property
    def start(self):
        """
        Get the "start" node for the level.
        """
        return self._start

    @property
    def tail(self):
        """
        Get the "tail" node for the level.
        """
        return self._tail

    @head.setter
    def head(self, node):
        """
        Update the "head" node for the level.
        """
        self._head = node

    @start.setter
    def start(self, node):
        """
        Add the "start" node for the level.
        """
        self._start.append(node)

    def update_start(self, start_nodes):
        """
        Update the "start" nodes for the level.
        """
        self._start = start_nodes

    @tail.setter
    def tail(self, node):
        """
        Update the "tail" node for the level.
        """
        self._tail = node
