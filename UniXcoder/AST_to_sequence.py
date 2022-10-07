from tree_sitter import Tree, Node


def one_to_one(root_node: Tree):
    # implenment the algorithm from unixcoder here
    sequence = ""
    name = root_node.text

    # Is Leaf
    if root_node.child_count == 0:
        sequence += name
    else:
        sequence += name + "::left"
        for node in root_node.children:
            sequence += one_to_one(node)
        sequence += name + "::right"
    return sequence
