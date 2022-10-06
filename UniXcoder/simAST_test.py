# import tree_sitter
from typing import List

import tree_sitter
from tree_sitter import Tree, Node

# TODO: define declarations
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


FS = []
def main_simp(attree: Tree, code: str):
    nodes = []
    for node in traverse_tree(attree):
        nodes.append(node)

    for node in nodes:
        if node.type in declarators or node.type in statements:
            FS.append(node)

    return simplify_AST(attree.root_node, code, FS)

def simplify_AST(root_node: Node, code: str, FS: List[Node]):
    for n in root_node.children:
        if n in FS or n.text in code:
            #process node in mapping
            #else continue to a next level
        simplify_AST(n, code, FS)

    return root_node




# https://github.com/tree-sitter/py-tree-sitter/issues/33#issuecomment-689426763
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







# def get_token(node):
#     token = ''
#     if isinstance(node, str):
#         token = node
#     elif isinstance(node, set):
#         token = 'Modifier'
#     elif isinstance(node,Node):
#         token = node.__class__.__name__
#     return token
#
# def get_sequence(node, sequence, father, fa, cd):
#     token, children = get_token(node), get_children(node)
#     if token in ['ForStatement', 'TypeDeclaration', 'ContinueStatement', 'ContinueStatement', 'BreakStatement', 'ThrowStatement','TryStatement','ReturnStatement','WhileStatement', 'DoStatement','SwitchStatement', 'IfStatement', 'MethodDeclaration', 'ConstructorDeclaration', 'ClassDeclaration', 'EnumDeclaration', 'FieldDeclaration', 'VariableDeclarator', 'LocalVariableDeclaration', 'VariableDeclaration', 'FormalParameter'] or token in cd:
#         sequence.append(token)
#         father.append(fa)
#         fa = len(sequence)-1
#     for child in children:
#         get_sequence(child,sequence,father,fa,cd)
#     #if token in ['ForStatement', 'WhileStatement', 'DoStatement','SwitchStatement', 'IfStatement', 'MethodDeclaration', 'ConstructorDeclaration', 'ClassDeclaration', 'EnumDeclaration', 'FieldDeclaration', 'VariableDeclarator', 'LocalVariableDeclaration', 'VariableDeclaration', 'FormalParameter']:
#     #    sequence.append('End')
#
#
#
# def get_sequences(node, sequence):
#     token, children = get_token(node), get_children(node)
#     sequence.append(token)
#     for child in children:
#         get_sequences(child,sequence)