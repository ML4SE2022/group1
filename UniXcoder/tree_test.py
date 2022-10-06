import torch
from unixcoder import UniXcoder

from tree_sitter import Language, Parser, Tree
from simAST_test import main_simp

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
int add(int a, int b)
{
  int result;
  result = a+b;
  return result;                  // return statement
}
""", "utf8"))
# print(tree.root_node.sexp())
# print(tree.root_node.text)
# print(tree.root_node.children[0].children[1].type)
# print(tree.root_node.children[0].children[1].text)
# print(tree.root_node.children[0].children[1].children[0].type)
# print(tree.root_node.children[0].children[1].children[0].text)
# print(tree.root_node.children[0].children[1].children[0].text)
# print(tree.root_node.children[0].children[1].children[1].type)
# print(33333333333333333333)
# print(tree.root_node.children[0].children[1].children[1].text)
# print(tree.root_node.children[0].children[1].children[1].children[0].type)
# print(tree.root_node.children[0].children[1].children[1].children[0].text)
# print(tree.root_node.children[0].children[1].children[1].children[1].type)
# print(tree.root_node.children[0].children[1].children[1].children[1].text)
# print(tree.root_node.children[0].children[1].children[1].children[1].children[0].type)
# print(tree.root_node.children[0].children[1].children[1].children[1].children[0].text)
# print(tree.root_node.children[0].children[1].children[1].children[1].children[1].type)
# print(tree.root_node.children[0].children[1].children[1].children[1].children[1].text)
# print(tree.root_node.children[0].children[1].children[1].children[1].children[1].children)
print(tree.root_node.sexp())
main_simp(tree)
print(tree.root_node.sexp())
