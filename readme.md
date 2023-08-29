# NetTree

Adapted from Wu et al., _A Nettree for Pattern Matching with Flexible Wildcard Constraints_, 2010.

Algorithm to solve the string matching problem with eventual wildcards.
The problem has bee, extended to multi-dimensional sequences with patterns that may span multiple sequences.

This is a rather loose implementation of the algorithm proposed in the original article, as it lacked several important technical details.  
As a result the following changes were made:

- The _data field_ of the Level class does not contain the common symbol associated to the nodes of this level, nor the total number of nodes. Instead, it contains a list containing all a reference to all nodes in the level.
- The _start pointer_ of the Level class is now a list that contains all nodes that can potentially occur in a pattern. Note that this list is iterated in reverse order to avoid a (unnecessary) pruning step.
- The Node class does not contain the number of its parents or the number of its children.
- The Node class does not contain a list of all of its children.
- The _next pointer_ in the Node class has been replaced by a _predecessor_ pointer, which - in tandem with the iteration in reverse order of the _start pointer_ list - works well during the parent-children relationship generation step to avoid (unnecessary) pruning.
