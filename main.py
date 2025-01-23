import astpretty
from graphviz import Digraph
from parser import parse
from tree import e
from tree import BinOp, Number, If

def visualize_ast(node, graph=None, parent=None, counter=None):
    """Recursively add nodes and edges to the Graphviz Digraph."""
    if graph is None:
        graph = Digraph(format="png")
        counter = {"count": 0}
    node_id = f"node{counter['count']}"
    counter['count'] += 1

    # Add the current node to the graph
    label = ""
    if isinstance(node, BinOp):
        label = f"BinOp({node.op})"
    elif isinstance(node, Number):
        label = f"Number({node.v})"
    elif isinstance(node, If):
        label = "If"
    else:
        label = "Unknown"

    graph.node(node_id, label)

    # Connect to the parent if not root
    if parent is not None:
        graph.edge(parent, node_id)

    # Add child nodes recursively
    if isinstance(node, BinOp):
        visualize_ast(node.left, graph, node_id, counter)
        visualize_ast(node.right, graph, node_id, counter)
    elif isinstance(node, If):
        visualize_ast(node.c, graph, node_id, counter)
        visualize_ast(node.t, graph, node_id, counter)
        visualize_ast(node.e, graph, node_id, counter)

    return graph


if __name__ == "__main__":
    expression = '2 + 5 * 6 / 2'
    tree = parse(expression)
    result = e(tree)
    astpretty.pprint(tree)

    # Print the result
    print(f"Result: {result}")

    # Visualize and save the AST
    graph = visualize_ast(tree)
    graph.render("ast_tree", view=True)
