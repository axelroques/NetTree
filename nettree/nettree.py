
from .plot import plot_patterns
from .level import Level
from .node import Node


class NetTree:

    def __init__(self, data, pattern, max_gap=2) -> None:

        # Store inputs
        self.data = data
        self.pattern = pattern
        self.max_gap = max_gap

        # Instantiate tree levels
        self._levels = [Level() for _ in range(len(pattern))]

        # Initialize empty patterns variable
        self._patterns = []

    def build(self):
        """
        Build the NetTree.
        """

        # Iterate over the input sequence
        for i_col, column in enumerate(self.data.T):

            print('\n\n\t i_col =', i_col, '; column =', column)

            # Iterate over the symbols in the pattern
            for i_symbol, symbol in enumerate(self.pattern):

                print('\t\t symbol =', symbol)

                # If one symbol in the column matches the first symbol
                # in the pattern
                if (i_symbol == 0) and (symbol in column):

                    # Add a root note
                    node = Node(
                        pos=(int(symbol[-1]), i_col),
                        predecessor=self._levels[0].tail
                    )
                    print('\t\t --> Adding root node:', node)
                    self._levels[0].add_node(node)

                    # A root node's path is equal to one
                    node.path = 1

                    # Also, if no head is present, add the current node as head
                    if not self._levels[0].head:
                        self._levels[0].head = node

                    # Update the root level's start nodes
                    self._levels[0].start = node

                    # Update the root level's tail node
                    self._levels[0].tail = node

                    # Move on to the next symbol
                    continue

                # If one symbol in the column matches any symbol in the pattern
                # excepted for the first symbol
                if (i_symbol != 0) and (symbol in column):

                    # Get the first possible start node  at the
                    # (i_symbol-1)th level
                    start_nodes = self._levels[i_symbol-1].start

                    # Check constraints
                    start_node = None
                    # Start nodes are iterated in inverse order because we explore
                    # the predecessors of the start node when creating parent-child
                    # relationships
                    for node in start_nodes[::-1]:
                        dist = i_col - node.pos[1] - 1

                        if (0 <= dist) and (dist <= self.max_gap):
                            start_node = node
                            break

                    # If constraints are not met, move on to the next symbol
                    if not start_node:
                        continue

                    # Otherwise, create a new node
                    node = Node(
                        pos=(int(symbol[-1]), i_col),
                        predecessor=self._levels[i_symbol].tail
                    )
                    print(f'\t\t --> Adding node {node} at level {i_symbol}')
                    self._levels[i_symbol].add_node(node)

                    # Update tail node on level i_symbol
                    self._levels[i_symbol].tail = node

                    # Update start nodes in level i_symbol-1
                    self._levels[i_symbol-1].update_start([
                        n for n in self._levels[i_symbol-1].start
                        if n != start_node
                    ])

                    # Update start nodes in level i_symbol
                    self._levels[i_symbol].start = node

                    # Add parent-child relationship
                    parent = start_node
                    while (parent) and \
                        (0 <= i_col-parent.pos[1]-1) and \
                            (i_col-parent.pos[1]-1 <= self.max_gap):

                        print(
                            f'\t\t --> Adding relationship: {parent} -> {node}')

                        # Add parent to the new node
                        node.parents = parent

                        # Also add path info to the new node
                        node.path += parent.path

                        # Check predecessor of parent
                        parent = parent.predecessor

    @property
    def occurrences(self):
        """
        Return number of occurences of the pattern in the tree.
        """
        return sum(node.path for node in self._levels[-1].nodes)

    @property
    def patterns(self):
        """
        Return the locations of the pattern in the input sequence.
        Here, a depth-first search is conducted starting from the 
        leaves of the tree.

        Remark: parents have to be iterated through in chronological 
        order, otherwise some parents may be marked as visited and 
        therefore not explored during the next iterations. 
        """

        # TO BE REMOVED
        self._patterns = []

        def DFS(node, visited=[], paths=[], stack=[]):
            """
            Recursive DFS algorithm.
            """

            # Update stack
            if node not in visited:
                stack.append(node)

            # Update visited nodes
            visited.append(node)

            # Check if the node is a root
            if not node.parents:
                # Store path
                paths.append(stack.copy()[::-1])

            # Climb up the tree
            for parent in node.parents[::-1]:

                # Check if the parent has not already been visited
                if parent not in visited:
                    DFS(parent, visited, paths, stack)

            # Pop last item on the stack and visited arrays
            stack.pop()
            visited.pop()

            return paths

        # If pattern locations were computed previously, simply return them
        if self._patterns:
            return self._patterns

        # Otherwise, run DFS for all leaf nodes
        else:
            self._patterns = []
            for node in self._levels[-1].nodes:
                self._patterns += DFS(node, [], [], [])

        return self._patterns

    def plot(self, i_pattern=0, show_symbols=True):
        """
        Plot patterns in the input data. 
        """
        plot_patterns(
            self.data, self._patterns, i_pattern, show_symbols
        )
