#!/usr/bin/env python3
from __future__ import annotations
from hashlib import sha256


class Tree:
    """Tree should never be instantiated.
    :param value: the merkle hash
    :param parent: should never be None, except for root
    """
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent

    def is_root(self):
        return self.parent is None

    def __repr__(self):
        return f'Node[value={self.value}, parent={self.parent}]'


class Node(Tree):
    def __init__(self, value, parent: Node, left: Tree, right: Tree):
        super().__init__(value, parent)
        self.left = left
        self.right = right


class Leaf(Tree):
    def __init__(self, value, parent: Node, block):
        super().__init__(value, parent)
        self.block = block


def create_leaves(chunks: [str]):
    leaves = []
    for chunk in chunks:
        chunk_hash = compute_hash(chunk)
        leaf = Leaf(chunk_hash, None, chunk)
        leaves.append(leaf)
    return leaves


def compute_hash(chunk: str):
    return sha256(chunk.encode('UTF-8')).hexdigest()


def create_tree(nodes: [Tree]):
    num_nodes = len(nodes)

    if num_nodes == 1:
        return nodes[0]

    parents = []

    i = 0
    while i < num_nodes:
        left_child = nodes[i]
        right_child = nodes[i + 1] if (i + 1 < num_nodes) else left_child

        parents.append(create_parent(left_child, right_child))

        i = i + 2

    return create_tree(parents)


def create_parent(left_child, right_child):
    combined_hash = compute_hash(left_child.value + right_child.value)
    parent = Node(combined_hash, None, left_child, right_child)
    left_child.parent = parent
    right_child.parent = parent
    return parent


def main():
    """Use-case (Beispiel)"""
    chunks = [str(i) for i in range(10)]
    leaves = create_leaves(chunks)
    return create_tree(leaves)


if __name__ == '__main__':
    main()
