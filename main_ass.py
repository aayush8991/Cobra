# import astpretty
# from graphviz import Digraph
from parser import *
from eval import *
from tree import *
from lexer import *
from resolver import *
from assembler import *

# def visualize_ast(node, graph=None, parent=None, counter=None):
#     """Recursively add nodes and edges to the Graphviz Digraph."""
#     if graph is None:
#         graph = Digraph(format="png")
#         counter = {"count": 0}
#     node_id = f"node{counter['count']}"
#     counter['count'] += 1

#     # Add the current node to the graph
#     label = ""
#     if isinstance(node, BinOp):
#         label = f"BinOp({node.op})"
#     elif isinstance(node, Token):
#         label = f"Token({node.v})"
#     elif isinstance(node, Fun):
#         label = f"Fun({node.n})"
#     elif isinstance(node, Call):
#         label = f"Call({node.n})"
#     elif isinstance(node, If):
#         label = "If"
#     elif isinstance(node, Let):
#         label = f"{node.v}"
#     elif isinstance(node, While):
#         label = "While"
#     elif isinstance(node, Var):
#         label = f"{node}"
#     else:
#         label = "Unknown"

#     graph.node(node_id, label)

#     # Connect to the parent if not root
#     if parent is not None:
#         graph.edge(parent, node_id)

#     # Add child nodes recursively
#     if isinstance(node, BinOp):
#         visualize_ast(node.left, graph, node_id, counter)
#         visualize_ast(node.right, graph, node_id, counter)
#     elif isinstance(node, Fun):
#         visualize_ast(node.b, graph, node_id, counter)
#         visualize_ast(node.e, graph, node_id, counter)
#     elif isinstance(node, Call):
#         visualize_ast(node.a, graph, node_id, counter)
#     elif isinstance(node, If):
#         visualize_ast(node.cond, graph, node_id, counter)
#         visualize_ast(node.then, graph, node_id, counter)
#         visualize_ast(node.else_, graph, node_id, counter)
#     elif isinstance(node, Let):
#         visualize_ast(node.e, graph, node_id, counter)
#         visualize_ast(node.f, graph, node_id, counter)
#     elif isinstance(node, While):
#         visualize_ast(node.condition, graph, node_id, counter)
#         visualize_ast(node.body, graph, node_id, counter)

#     return graph


if __name__ == "__main__":
  
    file_path = "code.txt"
    try:
        with open(file_path, "r") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit(1)

    ast = parse(code)
    # print(ast)
    # graph = visualize_ast(ast)
    # graph.render("ast_tree", view=True)

    print("-------------------------------------")
    abt = resolve(ast)

    # result = e(abt)
    # print(f"Result: {result}")

    bytecode = codegen(abt)
    print("Bytecode:", bytecode)

    with open("program.bin", "wb") as f:
        f.write(bytecode)

    # print("Bytecode saved to program.bin")