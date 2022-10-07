
from tree_sitter import Language, Parser, Tree, Node
# import tree_sitter
from typing import List

declarators = ["array_declarator", "attributed_declarator", "destructor_name", "function_declarator", "identifier",
                "operator_name", "parenthesized_declarator", "pointer_declarator", "qualified_identifier", "reference_declarator",
                "structured_binding_declarator", "template_function"]

declarations = ["declaration", "attribute_declaration", "alias_declaration", "static_assert_declaration", "template_declaration",
                "using_declaration", "friend_declaration", "field_declaration", "parameter_declaration", "optional_parameter_declaration",
                "variadic_parameter_declaration"]

statements = ["attributed_statement", "break_statement", "case_statement", "co_return_statement", "co_yield_statement",
              "compound_statement", "continue_statement", "do_statement", "expression_statement", "for_range_loop", "for_statement",
              "goto_statement", "if_statement", "labeled_statement", "return_statement", "switch_statement", "throw_statement",
              "try_statement", "while_statement"]

Language.build_library(
  # Store the library in the `build` directory
  'build/my-languages.so',

  # Include one or more languages
  # Add your own path
  [
    '.\\TreeSitter\\tree-sitter-cpp',
  ]
)

cpp_lang = Language('build/my-languages.so', 'cpp')

parser = Parser()
parser.set_language(cpp_lang)

# https://github.com/tree-sitter/tree-sitter-cpp/blob/master/test/corpus/types.txt
code = bytes("""
    int add(int a, int b)
    {
      int result;
      result = a+b;
      return result;                  // return statement
    }
    """, "utf8")

tree = parser.parse(code)

def preprocess(ast_tree: Tree, code: str):
    nodes = []
    FS = []
    for node in traverse_tree(ast_tree):
        nodes.append(node)

    for node in nodes:
        if node.type in declarators or node.type in statements:
            FS.append(node)
    
    return one_to_one(ast_tree, code, FS)

def traverse_tree(tree: Tree):
  cursor = tree.walk()

  reached_root = False
  while reached_root == False:
    yield cursor.node

    if cursor.goto_first_child():
      continue

    if cursor.goto_next_sibling():
      continue

    retracing = True
    while retracing:
      if not cursor.goto_parent():
        retracing = False
        reached_root = True

      if cursor.goto_next_sibling():
        retracing = False

def one_to_one(root_node: Tree, code: str, FS: List[Node]):
    # implenment the algorithm from unixcoder here
    sequence = ""
    name = root_node.type

    # Check here for node?
    if root_node in FS or root_node.type in code:
        # Is Leaf
        if root_node.child_count == 0:
            sequence += name
        else:
            sequence += name + "::left"
            for node in root_node.children:
                sequence += one_to_one(node, code, FS)
            sequence += name + "::right"
        return sequence
    else:
        for node in root_node.children:
            sequence += one_to_one(node, code, FS)
    return sequence

print(preprocess(tree.root_node, code.decode("utf-8")))
