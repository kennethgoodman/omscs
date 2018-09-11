# Copyright (C) 2013 Brian Wesley Baugh
# CSCE 6933: Social Network Analysis
# Created: January 22, 2013
# Updated: January 30, 2013
# FROM: https://gist.github.com/bwbaugh/4602818
"""Generate a randomly connected graph with N nodes and E edges."""
import random
import argparse
from pprint import pprint


class Graph(object):
    def __init__(self, nodes, edges=None, loops=False, multigraph=False,
                 digraph=False):
        self.nodes = nodes
        if edges:
            self.edges = edges
            self.edge_set = self._compute_edge_set()
        else:
            self.edges = []
            self.edge_set = set()
        self.loops = loops
        self.multigraph = multigraph
        self.digraph = digraph

    def add_edge(self, edge):
        """Add the edge if the graph type allows it."""
        if self.multigraph or edge not in self.edge_set:
            self.edges.append(edge)
            self.edge_set.add(edge)
            if not self.digraph:
                self.edge_set.add(edge[::-1])  # add other direction to set.
            return True
        return False

    def make_random_edge(self):
        """Generate a random edge between any two nodes in the graph."""
        if self.loops:
            # With replacement.
            random_edge = (random.choice(self.nodes), random.choice(self.nodes))
        else:
            # Without replacement.
            random_edge = tuple(random.sample(self.nodes, 2))
        return random_edge

    def add_random_edges(self, total_edges):
        """Add random edges until the number of desired edges is reached."""
        while len(self.edges) < total_edges:
            self.add_edge(self.make_random_edge())



def check_num_edges(nodes, num_edges, loops, multigraph, digraph):
    """Checks that the number of requested edges is acceptable."""
    num_nodes = len(nodes)
    # Check min edges
    min_edges = num_nodes - 1
    if num_edges < min_edges:
        raise ValueError('num_edges less than minimum (%i)' % min_edges)
    # Check max edges
    max_edges = num_nodes * (num_nodes - 1)
    if not digraph:
        max_edges /= 2
    if loops:
        max_edges += num_nodes
    if not multigraph and num_edges > max_edges:
            raise ValueError('num_edges greater than maximum (%i)' % max_edges)


def naive(nodes, num_edges, loops=False, multigraph=False, digraph=False):
    # Idea:
    # Each node starts off in its own component.
    # Keep track of the components, combining them when an edge merges two.
    # While there are less edges than requested:
    #     Randomly select two nodes, and create an edge between them.
    # If there is more than one component remaining, repeat the process.

    check_num_edges(nodes, num_edges, loops, multigraph, digraph)

    def update_components(components, edge):
        # Update the component list.
        comp_index = [None] * 2
        for index, comp in enumerate(components):
            for i in (0, 1):
                if edge[i] in comp:
                    comp_index[i] = index
            # Break early once we have found both sets.
            if all(x is not None for x in comp_index):
                break
        # Combine components if the nodes aren't already in the same one.
        if comp_index[0] != comp_index[1]:
            components[comp_index[0]] |= components[comp_index[1]]
            del components[comp_index[1]]

    finished = False
    while not finished:
        graph = Graph(nodes, loops=loops, multigraph=multigraph, digraph=digraph)
        # Start with each node in its own component.
        components = [set([x]) for x in nodes]
        while len(graph.edges) < num_edges:
            # Generate a random edge.
            edge = graph.make_random_edge()
            if graph.add_edge(edge):
                # Update the component list.
                update_components(components, edge)
        if len(components) == 1:
            finished = True

    return graph


def partition(nodes, num_edges, loops=False, multigraph=False, digraph=False):
    # Algorithm inspiration:
    # http://stackoverflow.com/questions/2041517/random-simple-connected-graph-generation-with-given-sparseness

    # Idea:
    # Create a random connected graph by adding edges between nodes from
    # different partitions.
    # Add random edges until the number of desired edges is reached.

    check_num_edges(nodes, num_edges, loops, multigraph, digraph)

    graph = Graph(nodes, loops=loops, multigraph=multigraph, digraph=digraph)

    # Create two partitions, S and T. Initially store all nodes in S.
    S, T = set(nodes), set()

    # Randomly select a first node, and place it in T.
    node_s = random.sample(S, 1).pop()
    S.remove(node_s)
    T.add(node_s)

    # Create a random connected graph.
    while S:
        # Select random node from S, and another in T.
        node_s, node_t = random.sample(S, 1).pop(), random.sample(T, 1).pop()
        # Create an edge between the nodes, and move the node from S to T.
        edge = (node_s, node_t)
        assert graph.add_edge(edge) == True
        S.remove(node_s)
        T.add(node_s)

    # Add random edges until the number of desired edges is reached.
    graph.add_random_edges(num_edges)

    return graph


def random_walk(nodes, num_edges, loops=False, multigraph=False, digraph=False):
    # Algorithm inspiration:
    # https://en.wikipedia.org/wiki/Uniform_spanning_tree#The_uniform_spanning_tree

    # Idea:
    # Create a uniform spanning tree (UST) using a random walk.
    # Add random edges until the number of desired edges is reached.

    check_num_edges(nodes, num_edges, loops, multigraph, digraph)

    # Create two partitions, S and T. Initially store all nodes in S.
    S, T = set(nodes), set()

    # Pick a random node, and mark it as visited and the current node.
    current_node = random.sample(S, 1).pop()
    S.remove(current_node)
    T.add(current_node)

    graph = Graph(nodes, loops=loops, multigraph=multigraph, digraph=digraph)

    # Create a random connected graph.
    while S:
        # Randomly pick the next node from the neighbors of the current node.
        # As we are generating a connected graph, we assume a complete graph.
        neighbor_node = random.sample(nodes, 1).pop()
        # If the new node hasn't been visited, add the edge from current to new.
        if neighbor_node not in T:
            edge = (current_node, neighbor_node)
            graph.add_edge(edge)
            S.remove(neighbor_node)
            T.add(neighbor_node)
        # Set the new node as the current node.
        current_node = neighbor_node

    # Add random edges until the number of desired edges is reached.
    graph.add_random_edges(num_edges)

    return graph

