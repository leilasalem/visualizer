"""Modelling CS Education research paper data
=== CSC148 Winter 2019 ===
This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.
All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Bogdan Simion, David Liu, Diane Horton, Jacqueline Smith
=== Module Description ===
This module contains a new class, PaperTree, which is used to model data on
publications in a particular area of Computer Science Education research.
This data is adapted from a dataset presented at SIGCSE 2019.
You can find the full dataset here: https://www.brettbecker.com/sigcse2019/
Although this data is very different from filesystem data, it is still
hierarchical. This means we are able to model it using a TMTree subclass,
and we can then run it through our treemap visualisation tool to get a nice
interactive graphical representation of this data.
"""
import csv
from typing import List, Dict
from tm_trees import TMTree

# Filename for the dataset
# TODO: fix indentation
DATA_FILE = 'cs1_papers.csv'

class PaperTree(TMTree):
    """A tree representation of Computer Science Education research paper data.
    === Private Attributes ===
    These should store information about this paper's <authors> and <doi>.
    _authors:
        The author of this paper.
    _doi:
        The doi of this paper.
    === Inherited Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.
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
    - All TMTree RIs are inherited.
    """
    _authors: str
    _doi: str

    def __init__(self, name: str, subtrees: List[TMTree], authors: str = '',
                 doi: str = '', citations: int = 0, by_year: bool = True,
                 all_papers: bool = False) -> None:
        """Initialize a new PaperTree with the given <name> and <subtrees>,
        <authors> and <doi>, and with <citations> as the size of the data.
        If <all_papers> is True, then this tree is to be the root of the paper
        tree. In that case, load data about papers from DATA_FILE to build the
        tree.
        If <all_papers> is False, Do NOT load new data.
        <by_year> indicates whether or not the first level of subtrees should be
        the years, followed by each category, subcategory, and so on. If
        <by_year> is False, then the year in the dataset is simply ignored.
        """
        TMTree.__init__(self, name, subtrees, citations)
        self._doi = doi
        self._authors = authors

        if all_papers:
            if not by_year:
                tree_list = _no_year_tree()
                for t in tree_list:
                    self._subtrees.append(t)
            else:
                tree_list = _by_year_tree()
                for t in tree_list:
                    self._subtrees.append(t)

            new_size = 0
            for subtree in self._subtrees:
                subtree._parent_tree = self
                subtree._parent_check()
                subtree._closed()
                x = subtree.update_data_sizes()
                new_size += x
            self.data_size = new_size
        else:
            pass
          
     
def _no_year_tree() -> List[PaperTree]:
    """Return list of first level subtrees from the data file.
    First level subtrees represent categories.
    """
    top_list = []
    name_list = []

    with open(SOFTY, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            leaf = PaperTree(row['Title'], [], row['Author'], row['Url'],
                             int(row['Citations']))
            cat_paper = row['Category'].split(': ')
            if cat_paper[0] not in name_list:
                leaves = [leaf]
                backward_cat = cat_paper[:]
                backward_cat.reverse()
                i = 0
                while i < len(backward_cat):
                    leaves.append(PaperTree(backward_cat[i], [leaves[i]]))
                    i += 1
                top_list.append(leaves[-1])
                name_list.append(cat_paper[0])
            else:
                i = 1
                find = name_list.index(cat_paper[0])
                parent = top_list[find]
                searching = parent._subtrees
                names = _names_list(searching)
                while (i < len(cat_paper)) and (cat_paper[i] in names):
                  #  i += 1
                    find = names.index(cat_paper[i])
                    parent = searching[find]
                    searching = parent._subtrees
                    names = _names_list(searching)
                    i += 1
                if i == len(cat_paper):
                    searching.append(leaf)
                    leaf._parent_tree = parent
                # path exists already
                else:
                    cate = cat_paper[i:]
                    searching.append(_path(cate, leaf))
                    # means partial path, create new path from i to paper

        csvfile.close()
        return top_list

def _by_year_tree() -> List[PaperTree]:
    """Return a list of first level subtrees from the data file.
    First level subtrees represent years, their subtrees are categories.
    """
    top_list = []
    years = []

    with open(SOFTY, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            leaf = PaperTree(row['Title'], [], row['Author'], row['Url'],
                             int(row['Citations']))
            cat_paper = row['Category'].split(': ')
            cat_paper.insert(0, row['Year'])
            if cat_paper[0] not in years:
                leaves = [leaf]
                backward_cat = cat_paper[:]
                backward_cat.reverse()
                i = 0
                while i < len(backward_cat):
                    leaves.append(PaperTree(backward_cat[i], [leaves[i]]))
                    i += 1
                top_list.append(leaves[-1])
                #years.append(leaves[-1]._name)
                years.append(cat_paper[0])
            else:
                i = 1
                find = years.index(cat_paper[0])
                parent = top_list[find]
                searching = parent._subtrees
                names = _names_list(searching)
                while (i < len(cat_paper)) and (cat_paper[i] in names):
                    #i += 1
                    find = names.index(cat_paper[i])
                    parent = searching[find]
                    searching = parent._subtrees
                    names = _names_list(searching)
                    i += 1
                if i == len(cat_paper):
                    searching.append(leaf)
                    leaf._parent_tree = parent
                else:
                    cate = cat_paper[i:]
                    searching.append(_path(cate, leaf))
                    # means partial path, create new path from i to paper

        csvfile.close()
        return top_list

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

def _path(cat: List[str], paper: PaperTree) -> PaperTree:
    """Return instance of PaperTree representing path from cat[0] to
    leaf <paper>.
    """
    leaves = [paper]
    backward_cat = cat
    backward_cat.reverse()
    i = 0
    while i < len(backward_cat):
        leaves.append(PaperTree(backward_cat[i], [leaves[i]]))
        i += 1
    return leaves[-1]

def _names_list(trees: List[TMTree]) -> List[str]:
    """Return list of names of the trees in list <trees>.
    """
    names = []
    for tree in trees:
        names.append(tree._name)
    return names


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'typing', 'csv', 'tm_trees'],
        'allowed-io': ['_children'],
        'max-args': 8
    })
