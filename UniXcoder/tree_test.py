import torch
from unixcoder import UniXcoder

from tree_sitter import Language, Parser

Language.build_library(
  # Store the library in the `build` directory
  'build/my-languages.so',

  # Include one or more languages
  # Add your own path
  [
    'C:\\Users\\Irene Park\\Desktop\\tree-sitter-cpp',
  ]
)

cpp_lang = Language('build/my-languages.so', 'cpp')

parser = Parser()
parser.set_language(cpp_lang)

# https://github.com/tree-sitter/tree-sitter-cpp/blob/master/test/corpus/types.txt
tree = parser.parse(bytes("""
void foo() {
  auto x = 1;
}
""", "utf8"))
print(tree.root_node.type)
print(tree.root_node.children[0].type)
print(tree.root_node.children[0].children[0].type)
print(tree.root_node.children[0].children[1].type)
print(tree.root_node.children[0].children[2].type)