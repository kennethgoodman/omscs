import argparse
import random
from random_connected_graphy import random_walk as rw_algo, partition as part_algo, naive as naive_algo
from collections import defaultdict


def generate_graph(num_nodes, num_edges, algo):
    nodes = list(range(1, num_nodes + 1))
    graph = algo(nodes, num_edges, False, False, False)
    return graph

def graph_to_topo(graph):
   topo = defaultdict(set)
   for edge in graph.edges:
      topo[edge[0]].add(edge[1])
      topo[edge[1]].add(edge[0])

   for n in topo:
      topo[n] = sorted(list(topo[n]))

   return topo

def topo_to_log(topo, topo_name):
   raise NotImplementedError()    

def topo_to_py(topo, filename):
    with open(filename, 'w') as f:
        f.write('\n\ntopo = {\n')
        keys = sorted(topo.keys())
        for key in keys:
            f.write('    {}:{},\n'.format(key, topo[key]))
        f.write('}')
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='random topo generator')
    parser.add_argument('-n', '--nodes', type=int, default=4,
                        help='number of nodes (default is 4)')
    parser.add_argument('-e', '--edges', type=int, 
                        help='number of edges (default is rand(nodes - 1, (nodes-1)*(nodes)/2))')
    parser.add_argument('-l', '--logname', type=str, default='random.Log',
                        help='name of log (default is random.Log)')
    parser.add_argument('-a', '--algo', type=str, default='randomwalk',
                        help='algo to genearte graph: randomwalk, partition, naive (deafult is randomwalk)')
    parser.add_argument('-t', '--toponame', type=str, default='randomtopo.py',
                        help='name of topo file (deafult is randomtopo.py)') 
    args = parser.parse_args()
    nodes = args.nodes or parser.get_default('nodes')
    default_edges = random.randint(nodes - 1, nodes * (nodes-1)//2)
    edges = args.edges
    if edges is None:
        edges = default_edges
    algo = args.algo
    if algo is None:
        algo = 'random walk'
    assert args.algo in ['randomwalk','partition','naive'], 'Must be in [randomwalk, partition, naive]'
    algo = {'randomwalk': rw_algo, 'partition': part_algo, 'naive': naive_algo}[algo]
    graph = generate_graph(nodes, edges, algo)
    topo = graph_to_topo(graph)
    topo_to_py(topo, args.toponame or parser.get_default('toponame'))
    # topo_to_log(topo, args.logname or parser.get_default('logname'))
