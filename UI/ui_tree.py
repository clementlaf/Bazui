"""This module contains the classes to manage the tree of the UI
"""

import pygame as pg

from ui_object import UiObject
from vector import Vector as vec

class Node:
    """Node class to manage the nodes of the tree
    """

    def __init__(self, uiobject: UiObject, parent=None, childs=None):
        self.object = uiobject
        self.parent = parent
        if childs is None:
            self.childs = []
        else:
            self.childs = childs

    def add_child(self, child: 'Node'):
        """Add a child to the node

        Args:
            child (Node): The child to add
        """

        self.childs.append(child)

    def remove_child(self, child: 'Node'):
        """Remove a child from the node

        Args:
            child (Node): The child to remove
        """

        self.childs.remove(child)

    def set_parent(self, parent: 'Node'):
        """Set the parent of the node

        Args:
            parent (Node): The parent of the node
        """

        self.parent = parent

    def is_root(self)-> bool:
        """Check if the node is the root of the tree

        Returns:
            bool: True if the node is the root of the tree, False otherwise
        """

        return self.parent is None

    def is_leaf(self)-> bool:
        """Check if the node is a leaf of the tree

        Returns:
            bool: True if the node is a leaf of the tree, False otherwise
        """

        return len(self.childs) == 0


class Tree:
    """Tree class to manage the nodes of the tree
    """

    def __init__(self, root):
        self.root = root

    def add_node(self, node: Node, parent: Node):
        """Add a node to the tree

        Args:
            node (Node): The node to add
            parent (Node): The parent of the node
        """

        parent.add_child(node)
        node.set_parent(parent)

    def remove_node(self, node: Node):
        """Remove a node from the tree

        Args:
            node (Node): The node to remove
        """

        node.parent.remove_child(node)
        node.parent = None
        node.childs = []

    def get_position_of(self, node: Node)-> vec:
        """Return the position of the node in the tree

        Args:
            node (Node): The node to get the position

        Returns:
            vec: The position of the node
        """

        if node.is_root():
            return node.object.pos
        else:
            if node.object.pos_type == "relative":
                return node.parent.object.pos + node.object.pos
            elif node.object.pos_type == "absolute":
                return node.object.pos
            else:
                raise ValueError("Invalid position type")

    def draw(self, screen: pg.Surface):
        """Draw the tree on the screen

        Args:
            screen (pg.Surface): The screen to draw the tree
        """

        self._draw_node(screen, self.root)

    def _draw_node(self, screen: pg.Surface, node: Node):
        """Draw the node on the screen"
        """

        node.object.draw(screen, self.get_position_of(node))
        for child in node.childs:
            self._draw_node(screen, child)
