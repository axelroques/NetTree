
from .plot import plot_patterns
from .symbol import Symbol
from .level import Level
from .node import Node
import numpy as np


class NetTree:

    def __init__(self, data, rule) -> None:

        # Store inputs
        self._raw_data = data
        self.rule = rule

        # Preprocess data
        self._preprocess()

        # Instantiate tree levels
        self._levels = [Level() for _ in range(len(rule))]

        # Initialize empty patterns variable
        self._patterns = []

    def _preprocess(self):
        """ 
        Convert input into a valid format.
        """

        # Check that rule columns are in the data
        if not set(r['series'] for r in self.rule).issubset(set(self._raw_data.columns)):
            raise RuntimeError(
                'Rule is invalid: all pattern columns are not contained in the data.'
            )
        
        # Check subrule validity
        for subrule in self.rule:
            self._subrule_check(subrule)

        # Check whether the data contains temporal information
        if not 't' in self._raw_data.columns:
            self._raw_data['t'] = np.arange(len(self._raw_data))

        # Create input array
        self.series_labels = [c for c in self._raw_data.columns if c != 't']
        self.data = np.empty((len(self.series_labels), len(self._raw_data)), dtype=object)
        for i_row in range(len(self._raw_data[:-1])):
            for i_col, col in enumerate(self.series_labels):
                symbol = self._raw_data.iloc[i_row, i_col]
                t = (
                    self._raw_data.loc[i_row, 't'],
                    self._raw_data.loc[i_row+1, 't']
                )
                symbol = Symbol(symbol, col, t)
                self.data[i_col, i_row] = symbol

        # Last slice
        for i_col, col in enumerate(self.series_labels):
            symbol = self._raw_data.iloc[i_row+1, i_col]
            t = (
                self._raw_data.loc[i_row+1, 't'],
                self._raw_data.loc[i_row+1, 't']
            )
            symbol = Symbol(symbol, col, t)
            self.data[i_col, -1] = symbol

    def _subrule_check(self, subrule):
        """
        Check sub-rule validity. 
        """

        # Check content of the rule for this column
        if not set(['symbol', 'series', 'op']).issubset(set(subrule.keys())):
            raise RuntimeError(
                f"Invalid keys in subrule {subrule}. Minimum expected keys: 'symbol', 'series', 'op'."
            )
        if not isinstance(subrule['op'], str):
            raise RuntimeError(
                f'Invalid operator type in subrule {subrule}. The operator should be a string.'
            )
        if 'gap' in subrule:
            if not (isinstance(subrule['gap'], tuple) and all(isinstance(x, (int, float)) for x in subrule['gap'])):
                raise RuntimeError(
                    f'Invalid gap type in subrule {subrule}. Expected tuple(int/float, int/float).'
                )
        # Default gap value
        if not 'gap' in subrule:
            subrule['gap'] = (0, 1)

    def build(self):
        """
        Build the NetTree.
        """
        print('data =', self.data)
        
        # Iterate over the input sequence, one slice at a time
        for i_slice, slice in enumerate(self.data.T):
            print('\n\n\t i_slice =', i_slice, '; slice =', slice)
            t_slice = self._raw_data.loc[i_slice, 't']

            # Iterate over the subrules in the pattern
            for i_subrule, subrule in enumerate(self.rule):
                
                # Get subrule info
                rule_symbol = subrule['symbol']
                rule_series = subrule['series']
                rule_op = subrule['op']
                rule_gap = subrule['gap']

                # Get slice symbol
                i_slice_symb = self.series_labels.index(rule_series)
                slice_symbol = slice[i_slice_symb]

                # NaN check
                try:
                    slice_symbol.symbol
                except AttributeError:
                    continue

                # Check subrule
                if not self._check_subrule(slice_symbol, rule_symbol, rule_op):
                    continue

                #############################
                # If it's the first subrule #
                #############################
                if i_subrule == 0:

                    # Add a root note
                    node = Node(
                        symbol=slice_symbol,
                        pos=(i_slice, i_slice_symb),
                        gap=rule_gap,
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
                
                #########################
                # Subrule number is > 1 #
                #########################
                # Get the first possible start node  at the
                # (i_symbol-1)th level
                start_nodes = self._levels[i_subrule-1].start

                # Check constraints
                start_node = None
                # Start nodes are iterated in inverse order because we explore
                # the predecessors of the start node when creating parent-child
                # relationships
                for node in start_nodes[::-1]:
                    if self._gap_check(t_slice, node):
                        start_node = node
                        break

                # If constraints are not met, move on to the next symbol
                if not start_node:
                    continue

                # Otherwise, create a new node
                node = Node(
                    symbol=slice_symbol,
                    pos=(i_slice, i_slice_symb),
                    gap=rule_gap,
                    predecessor=self._levels[i_subrule].tail
                )
                print(f'\t\t --> Adding node {node} at level {i_subrule}')
                self._levels[i_subrule].add_node(node)

                # Update tail node on level i_symbol
                self._levels[i_subrule].tail = node

                # Update start nodes in level i_symbol-1
                self._levels[i_subrule-1].update_start([
                    n for n in self._levels[i_subrule-1].start
                    if n != start_node
                ]) # Might be an issue here?

                # Update start nodes in level i_symbol
                self._levels[i_subrule].start = node

                # Add parent-child relationship
                parent = start_node
                while (parent) and self._gap_check(t_slice, parent):
                    print(
                        f'\t\t --> Adding relationship: {parent} -> {node}')

                    # Add parent to the new node
                    node.parents = parent

                    # Also add path info to the new node
                    node.path += parent.path

                    # Check predecessor of parent
                    parent = parent.predecessor

    def _check_subrule(self, slice_symbol, rule_symbol, op):
        """
        Check if the subrule criterion is met for one of the symbols
        in the column.
        """
        # print('\t\t\t Criterion =', symbol._operator[op](val))
        return slice_symbol._operator[op](rule_symbol)
    
    @staticmethod
    def _gap_check(t_slice, node):
        """ 
        Check whether the distance between the node and the slice respects
        the gap constraints.
        """
        dist = t_slice - node.symbol.t[0]
        print('DIST', dist)
        return (node.gap[0] <= dist) and (dist <= node.gap[1])

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

    def plot(self, i_pattern=0, show_symbols=False):
        """
        Plot patterns in the input data. 
        """
        plot_patterns(
            self.data, self.series_labels, self._patterns, i_pattern, show_symbols
        )
