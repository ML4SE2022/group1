import torch
import sys
import os
sys.path.append(r'../../../../UniXcoder')
from unixcoder import UniXcoder

from tree_sitter import Language, Parser

Language.build_library(
  # Store the library in the `build` directory
  'build/my-languages.so',

  # Include one or more languages
  # Add your own path
  [
    'D:\\tree-sitter-cpp',
  ]
)

cpp_lang = Language('build/my-languages.so', 'cpp')

parser = Parser()
parser.set_language(cpp_lang)

# https://github.com/tree-sitter/tree-sitter-cpp/blob/master/test/corpus/types.txt
tree = parser.parse(bytes("""
int add(int a, int b)
{
  int result;
  result = a+b;
  return result;                  // return statement
}
""", "utf8"))
print(tree.root_node.type)
print(tree.root_node.children[0].type)
print(tree.root_node.children[0].children[0].type)
print(tree.root_node.children[0].children[1].type)
print(tree.root_node.children[0].children[1].type)
print(tree.root_node.children[0].children[2].text)
print(tree.root_node.sexp())


def preprocess(ast_tree: Tree, code: str):
    nodes = []
    for node in traverse_tree(attree):
        nodes.append(node)

    for node in nodes:
        if node.type in declarators or node.type in statements:
            FS.append(node)
    
    return one_to_one(root_node, code, FS)

def one_to_one(root_node: Tree, code: str, FS: List[Node]):
    # implenment the algorithm from unixcoder here
    sequence = ""
    name = root_node.text

    # Check here for node?

    # Is Leaf
    if root_node.child_count == 0:
        sequence += name
    else:
        sequence += name + "::left"
        for node in root_node.children:
            sequence += one_to_one(node, code, FS)
        sequence += name + "::right"
    return sequence