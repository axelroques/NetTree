# NetTree

## In theory

Adapted from Wu et al., _A Nettree for Pattern Matching with Flexible Wildcard Constraints_, 2010.

The original method is a pattern matching algorithm with flexible wildcard constraints.
The algorithm has been extended to multi-dimensional inputs (with patterns that may span multiple sequences).
Furthermore, the notion of pattern was extended into a rule-like concept that allows the matching between two symbols beyond the '=' operator.
In short, one can search for all symbols such that $s \geq b$ rather than simply $s = b$.

This is a rather loose implementation of the algorithm proposed in the original article, as it lacked several important technical details.  
As a result the following changes were made:

- The _data field_ of the Level class does not contain the common symbol associated to the nodes of this level, nor the total number of nodes. Instead, it contains a list containing all a reference to all nodes in the level.
- The _start pointer_ of the Level class is now a list that contains all nodes that can potentially occur in a pattern. Note that this list is iterated in reverse order to avoid a (unnecessary) pruning step.
- The Node class does not contain the number of its parents or the number of its children.
- The Node class does not contain a list of all of its children.
- The _next pointer_ in the Node class has been replaced by a _predecessor_ pointer, which - in tandem with the iteration in reverse order of the _start pointer_ list - works well during the parent-children relationship generation step to avoid (unnecessary) pruning.

## In practice

The input data should be a pandas DataFrame, where each column should correspond to a sequence of symbols.
```python
df = pd.DataFrame(data={
    's_0': ['a', 'c', 'b', 'a', 'a', 'a', 'a'],
    's_1': ['e', 'b', 'd', 'a', 'b', 'c', 'b'],
    's_2': ['a', 'b', 'a', 'b', 'c', 'b', 'b']
})
```
The DataFrame may contain an optional 't' column with temporal information.

The pattern to be matched to the data should be expressed as a list of dictionaries, where each dictionary describes the symbol that should be matched and its characteristics.
```python
rule = [
    {
        'symbol': 'a',
        'series': 's_0',
        'op': '=',
        'gap': (1, 1),
    },
    {
        'symbol': 'a',
        'series': 's_0', 
        'op': '=',
        'gap': (0, 1),
    },
    {
        'symbol': 'b',
        'series': 's_2',
        'op': '=',
        'gap': (0, 1),
    }
]
```
The previous example searches for the (exact) pattern $\left[ a, a, b \right]$ (due to the '=' operator) where the first two symbols appear in series $0$, $0$, and $2$ respectively. 
The gap between the first and second symbols is at least $1$ and at most $1$, and the gap between the second and the third symbol is at least $0$ and at most $1$.

A NetTree can be built with:
```python
tree = NetTree(data=df, rule=rule)
tree.build()
```

Patterns can then be identified using:
```python
tree.patterns
```