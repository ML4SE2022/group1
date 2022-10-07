from tree_sitter import Tree, Node, Language, Parser

def one_to_one(root_node: Node):
    # implenment the algorithm from unixcoder here
    sequence = ""
    name = root_node.type

    # Is Leaf
    if root_node.child_count == 0:
        sequence += name
    else:
        sequence += name + "::left"
        for node in root_node.children:
            sequence += one_to_one(node)
        sequence += name + "::right"
    return sequence


Language.build_library(
  # Store the library in the `build` directory
  'build/my-languages.so',

  # Include one or more languages
  # Add your own path
  [
    '..\\TreeSitter\\tree-sitter-cpp',
  ]
)

cpp_lang = Language('build/my-languages.so', 'cpp')

parser = Parser()
parser.set_language(cpp_lang)

tree = parser.parse(bytes("""
int add(int a, int b)
{
  int result;
  result = a+b;
  return result;                  // return statement
}
""", "utf8"))

result = one_to_one(tree.root_node)

print(result)

