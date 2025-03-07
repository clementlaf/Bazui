
class Node:
    """Node class to manage the nodes of the tree
    """

    def __init__(self, object, parent=None, childs=None):
        self.object = object
        self.parent = parent
        if childs is None:
            self.childs = []
        else:
            self.childs = childs

    def add_child(self, child):
        """Add a child to the node

        Args:
            child (_type_): _description_
        """

        self.childs.append(child)

    def remove_child(self, child):
        """Remove a child from the node

        Args:
            child (_type_): _description_
        """

        self.childs.remove(child)

    def set_parent(self, parent):
        """Set the parent of the node

        Args:
            parent (_type_): _description_
        """

        self.parent = parent

    def is_root(self):
        """Check if the node is the root of the tree

        Returns:
            _type_: _description_
        """

        return self.parent is None

    def is_leaf(self):
        """Check if the node is a leaf of the tree

        Returns:
            _type_: _description_
        """

        return len(self.childs) == 0


class Tree:
    """Tree class to manage the nodes of the tree
    """

    def __init__(self, root):
        self.root = root

    def add_node(self, node, parent):
        """Add a node to the tree

        Args:
            node (_type_): _description_
            parent (_type_): _description_
        """

        parent.add_child(node)
        node.set_parent(parent)

    def remove_node(self, node):
        """Remove a node from the tree

        Args:
            node (_type_): _description_
        """

        node.parent.remove_child(node)
        node.parent = None
        node.childs = []
