"""Assignment 2: Trees for Treemap

=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""
from __future__ import annotations
import os
import math
from random import randint
from typing import List, Tuple, Optional


class TMTree:
    """A TreeMappableTree: a tree that is compatible with the treemap
    visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you implementing new public
    *methods* for this interface.
    You should not add any new public methods other than those required by
    the client code.
    You can, however, freely add private methods as needed.

    === Public Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.

    === Private Attributes ===
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.

    - _colour's elements are each in the range 0-255.

    - If _name is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.

    - if _parent_tree is not None, then self is in _parent_tree._subtrees

    - if _expanded is True, then _parent_tree._expanded is True
    - if _expanded is False, then _expanded is False for every tree
      in _subtrees
    - if _subtrees is empty, then _expanded is False
    """

    rect: Tuple[int, int, int, int]
    data_size: int
    _colour: Tuple[int, int, int]
    _name: str
    _subtrees: List[TMTree]
    _parent_tree: Optional[TMTree]
    _expanded: bool

    def __init__(self, name: str, subtrees: List[TMTree],
                 data_size: int = 0) -> None:
        """Initialize a new TMTree with a random colour and the provided <name>.

        If <subtrees> is empty, use <data_size> to initialize this tree's
        data_size.

        If <subtrees> is not empty, ignore the parameter <data_size>,
        and calculate this tree's data_size instead.

        Set this tree as the parent for each of its subtrees.

        Precondition: if <name> is None, then <subtrees> is empty.
        """
        self.rect = (0, 0, 0, 0)
        self._name = name
        self._subtrees = subtrees[:]
        self._parent_tree = None

        # You will change this in Task 5
        # if len(self._subtrees) > 0:
        #    self._expanded = True
        # else:
        #    self._expanded = False
        self._expanded = False

        x = randint(0, 255)
        y = randint(0, 255)
        z = randint(0, 255)
        self._colour = (x, y, z)

        if name is None:
            self.data_size = data_size #optional parameter 0 passed in
        elif subtrees == []:
            self.data_size = data_size #if file then its size would be passed in
        else:
            new_size = 0
            for subtree in subtrees:
                subtree._parent_tree = self
                subtree._expanded = False
                new_size += subtree.data_size
            self.data_size = new_size

    def is_empty(self) -> bool:
        """Return True iff this tree is empty.
        """
        return self._name is None

    def update_rectangles(self, rect: Tuple[int, int, int, int]) -> None:
        """Update the rectangles in this tree and its descendents using the
        treemap algorithm to fill the area defined by pygame rectangle <rect>.
        """
        if self.data_size == 0:
            pass
        elif self._subtrees == []:
            self.rect = rect
        else:
            self.rect = rect
            width = rect[2]
            height = rect[3]
            total = self.data_size
            if width > height:
                self._wide_update(rect, total)
            elif height >= width:
                self._tall_update(rect, total)

    def _wide_update(self, rect: Tuple[int, int, int, int], total: int) -> None:
        """Helper function for update_rectangles, handles cases where
        width is greater than height.
        """
        x, y, width, height = rect
        i = 0
        last = (len(self._subtrees) - 1)
        while i in range(len(self._subtrees)):
            if i == last:
                proportion = self._subtrees[i].data_size / total
                new_width = proportion * width
                self._subtrees[i].rect = x, y, math.ceil(
                    new_width), height
                x = x + math.ceil(new_width)
                self._subtrees[i].update_rectangles(
                    self._subtrees[i].rect)
            else:
                proportion = self._subtrees[i].data_size / total
                new_width = proportion * width
                self._subtrees[i].rect = x, y, math.trunc(
                    new_width), height
                x = x + math.trunc(new_width)
                self._subtrees[i].update_rectangles(
                    self._subtrees[i].rect)
            i += 1

    def _tall_update(self, rect: Tuple[int, int, int, int], total: int) -> None:
        x, y, width, height = rect
        i = 0
        last = (len(self._subtrees) - 1)
        while i in range(len(self._subtrees)):
            if i == last:
                proportion = self._subtrees[i].data_size / total
                new_height = proportion * height
                self._subtrees[i].rect = x, y, width, math.ceil(
                    new_height)
                y = y + math.ceil(new_height)
                self._subtrees[i].update_rectangles(
                    self._subtrees[i].rect)
            else:
                proportion = self._subtrees[i].data_size / total
                new_height = proportion * height
                self._subtrees[i].rect = x, y, width, math.trunc(
                    new_height)
                y = y + math.trunc(new_height)
                self._subtrees[i].update_rectangles(
                    self._subtrees[i].rect)
            i += 1

    def get_rectangles(self) -> List[Tuple[Tuple[int, int, int, int],
                                           Tuple[int, int, int]]]:
        """Return a list with tuples for every leaf in the displayed-tree
        rooted at this tree. Each tuple consists of a tuple that defines the
        appropriate pygame rectangle to display for a leaf, and the colour
        to fill it with.
        """
        if self.data_size == 0:
            return []
        elif self._subtrees == []:
            rect_up = self.rect, self._colour
            return [rect_up]
        elif not self._expanded:
            rect_up = self.rect, self._colour
            return [rect_up]
        else:
            the_rect = []
            for subtree in self._subtrees:
                the_rect.extend(subtree.get_rectangles())
            return the_rect

    def get_tree_at_position(self, pos: Tuple[int, int]) -> Optional[TMTree]:
        """Return the leaf in the displayed-tree rooted at this tree whose
        rectangle contains position <pos>, or None if <pos> is outside of this
        tree's rectangle.

        If <pos> is on the shared edge between two rectangles, return the
        tree represented by the rectangle that is closer to the origin.
        """
        a, b, c, d = self._get_rect()
        x, y = pos
        if not (a <= x <= c and b <= y <= d):
            return None
        elif self._subtrees == []:
            return self
        elif not self._expanded:
            return self
        else:
            for subtree in self._subtrees:
                result = subtree.get_tree_at_position(pos)
                if result is not None:
                    return result
            return None

    def _get_rect(self) -> Tuple[int, int, int, int]:
        """Return tuple of upper left coordinates and lower right coordinates.
        >>>self.rect
        (2, 4, 6, 8)
        >>>self._get_rect()
        (2, 4, 8, 12)
        """
        x, y, a, b = self.rect
        j = x + a
        k = y + b
        return x, y, j, k

    def update_data_sizes(self) -> int:
        """Update the data_size for this tree and its subtrees, based on the
        size of their leaves, and return the new size.

        If this tree is a leaf, return its size unchanged.
        """
        if self._name is None:
            return 0
        elif self._subtrees == []:
            return self.data_size
        else:
            new_size = 0
            for subtree in self._subtrees:
                new_size += subtree.update_data_sizes()
            self.data_size = new_size
            return self.data_size

    def move(self, destination: TMTree) -> None:
        """If this tree is a leaf, and <destination> is not a leaf, move this
        tree to be the last subtree of <destination>. Otherwise, do nothing.
        """
        if self._subtrees == [] and destination._subtrees != []:
            self._parent_tree._subtrees.remove(self)
            self._parent_tree = destination
            destination._subtrees.append(self)
            return None
        else:
            return None

    def change_size(self, factor: float) -> None:
        """Change the value of this tree's data_size attribute by <factor>.

        Always round up the amount to change, so that it's an int, and
        some change is made.

        Do nothing if this tree is not a leaf.
        """
        if self._subtrees != []:
            return None
        elif self.data_size == 0:
            return None
        else:
            if factor > 0:
                new_size = math.ceil(self.data_size * (1 + factor))
                if new_size >= 1:
                    self.data_size = new_size
                    return None
                else:
                    return None
            elif factor < 0:
                new_size = math.floor(self.data_size * (1 + factor))
                if new_size >= 1:
                    self.data_size = new_size
                    return None
                else:
                    return None
            else:
                return None

    def expand(self) -> None:
        """Set the value of this tree's _expanded attribute to True, adding
        the tree's children to the displayed tree.
        If this tree is a leaf, do nothing.

        Precondition: parent tree of selected is expanded
        """
        if self.data_size == 0:
            pass
        elif self._subtrees == []:
            pass
        else:
            self._expanded = True

    def expand_all(self) -> None:
        """Fully expand the tree rooted at selected tree in displayed tree.
        Set its, and all of its descendants' _expanded attributes to True,
        such that all leaves will be added to the displayed tree.
        If selected tree is a leaf, do nothing.

        Precondition: parent tree of selected is expanded
        """
        if self.data_size == 0:
            pass
        elif self._subtrees == []:
            pass
        else:
            self._expanded = True
            for subtree in self._subtrees:
                subtree.expand_all()

    def collapse(self) -> None:
        """The parent of selected rectangle will have its _expanded attribute
        set to False, and rectangle will not be shown in displayed tree.
        If _parent_tree is None (selected is root of whole tree) do nothing.
        """
        if self._parent_tree is None:
            pass
        elif self._subtrees == []:
            self._parent_tree._expanded = False
            #self._parent_tree._expanded = False
            for subtree in self._parent_tree._subtrees:
                subtree._expanded = False
        else:
            for subtree in self._parent_tree._subtrees:
                subtree.collapse()
            #for subtree in self._subtrees:
            #    subtree.collapse()
            # self._expanded = False
            # self._parent_tree._expanded = False

    def collapse_all(self) -> None:
        """The entire displayed tree will be collapsed down to single node.
        Parent of selected rectangle will be set to None, as will the parent's
        parent, and so on until the root's _expanded attribute is False.
        i.e. displayed tree will be single node
        If displayed tree is already single node, do nothing.
        """
        if self._parent_tree is None:
            self._expanded = False
            for subtree in self._subtrees:
                subtree.collapse_all()
        else:
            self._parent_tree.collapse_all()

    # Methods for the string representation
    def get_path_string(self, final_node: bool = True) -> str:
        """Return a string representing the path containing this tree
        and its ancestors, using the separator for this tree between each
        tree's name. If <final_node>, then add the suffix for the tree.
        """
        if self._parent_tree is None:
            path_str = self._name
            if final_node:
                path_str += self.get_suffix()
            return path_str
        else:
            path_str = (self._parent_tree.get_path_string(False) +
                        self.get_separator() + self._name)
            if final_node or len(self._subtrees) == 0:
                path_str += self.get_suffix()
            return path_str

    def _closed(self) -> None:
        """Set this tree's _expanded attribute to False.
        """
        self._expanded = False

    def _parent_check(self) -> None:
        """Go through subtrees and make sure that, if they have subtrees,
        they are the parent of them. If leaf, do nothing.

        Precondition: this tree is not empty.
        """
        if self._subtrees == []:
            pass
        else:
            for subtree in self._subtrees:
                if subtree._parent_tree == self:
                    pass
                else:
                    subtree._parent_tree = self
                    subtree._parent_check()

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        raise NotImplementedError

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        raise NotImplementedError

class FileSystemTree(TMTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _name attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/Diane/csc148/assignments'

    The data_size attribute for regular files is simply the size of the file,
    as reported by os.path.getsize.
    """

    def __init__(self, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        if os.path.isfile(path):
            TMTree.__init__(
                self, os.path.basename(path), [], os.path.getsize(path))

        elif os.path.isdir(path):
            contents = []
            for thing in os.listdir(path):
                new = os.path.join(path, thing)
                contents.append(FileSystemTree(new))
            TMTree.__init__(
                self, os.path.basename(path), contents)

    def get_separator(self) -> str:
        """Return the file separator for this OS.
        """
        return os.sep

    def get_suffix(self) -> str:
        """Return the final descriptor of this tree.
        """
        if len(self._subtrees) == 0:
            return ' (file)'
        else:
            return ' (folder)'


if __name__ == '__main__':

    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'python_ta', 'typing', 'math', 'random', 'os', '__future__'
        ]
    })
