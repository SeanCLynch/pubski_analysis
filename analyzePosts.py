# Run analysis on all .edgelist files.
# Run with: python analyzePosts.py 

import networkx as nx
import matplotlib.pyplot as plt
import csv

NUM_HUBS = 300

for idx in range (0, NUM_HUBS):

    # 1. Read edgelist file & create graph.
    graph = nx.read_edgelist("./pubski_data/%s.edgelist" % (idx), create_using=nx.DiGraph())

    # Draw graph for funzies.
    pos = nx.spring_layout(graph)
    node_colors = ['#10BDBB'] * len(graph.nodes())
    node_colors[1] = '#F37901'
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors)
    nx.draw_networkx_labels(graph, pos, font_size=8)
    nx.draw_networkx_edges(graph, pos, edge_color='#8097A4', connectionstyle='arc3,rad=0.2', arrowsize=12)
    # plt.show()

    # ----------------------------------------------------------------------------------------------
    # 2. Do analytics! 
    # There are so many: https://networkx.github.io/documentation/stable/reference/index.html
    # print(nx.info(graph))

    num_nodes = len(graph.nodes())
    num_edges = len(graph.edges())
    degrees = nx.degree_histogram(graph)
    avg_degree = float('%.3f'%(sum(degrees) / len(degrees)))
    print('\nbasic info', num_nodes, num_edges, avg_degree)

    # number of edges over number of possible edges. d = m / n(n-1)
    density = float('%.3f'%nx.density(graph))
    print('density', density)

    # Centrality Measures 

    # the degree centrality for a node v is the fraction of nodes it is connected to.
    degree_centralities = nx.degree_centrality(graph)
    dcs = [n for _, n in degree_centralities.items()]
    avg_degree_centrality = float('%.3f'%(sum(dcs) / len(dcs)))
    min_degree_centrality = float('%.3f'%min(degree_centralities.values()))
    max_degree_centrality = float('%.3f'%max(degree_centralities.values()))
    print('degree centrality', avg_degree_centrality, min_degree_centrality, max_degree_centrality)

    # eigenvector centrality computes the centrality for a node based on the centrality of its neighbors.
    try: 
        eigenvector_centralities = nx.eigenvector_centrality(graph)
        ecs = [n for _, n in eigenvector_centralities.items()]
        avg_ecs = float('%.3f'%(sum(ecs) / len(ecs)))
        min_ecs = float('%.3f'%min(eigenvector_centralities.values()))
        max_ecs = float('%.3f'%max(eigenvector_centralities.values()))
        print('eigenvector centrality', avg_ecs, min_ecs, max_ecs)
    except: 
        avg_ecs = -1
        min_ecs = -1
        max_ecs = -1

    # betweenness centrality of a node v is the sum of the fraction of all-pairs shortest paths that pass through v
    betweenness_centralities = nx.betweenness_centrality(graph)
    bcs = [n for _, n in betweenness_centralities.items()]
    avg_bcs = float('%.3f'%(sum(bcs) / len(bcs)))
    min_bcs = float('%.3f'%min(betweenness_centralities.values()))
    max_bcs = float('%.3f'%max(betweenness_centralities.values()))
    print('betweenness centrality', avg_bcs, min_bcs, max_bcs)

    # Clique Measures

    # the max subgraph of nodes which are all adjacent to each other. 
    from networkx.algorithms.approximation import clique
    max_clique = clique.max_clique(graph)
    max_clique_size = len(max_clique)
    print('max clique size', max_clique, max_clique_size)

    # Clustering Measures

    # num closed triplets / num total triplets - measure the degree of nodes tending to cluster together.
    clustering_coefficient = nx.average_clustering(graph)
    clustering_coefficient = float('%.3f'%clustering_coefficient)
    print('clustering coefficient', clustering_coefficient)

    # compute graph transitivity, the fraction of all possible triangles present in G.
    transitivity = nx.transitivity(graph)
    transitivity = float('%.3f'%transitivity)
    print('transitivity', transitivity)

    # Community Measures * 

    # from networkx.algorithms import community
    # a lot of these are for finding community within a graph
    # whereas we are finding community across graphs...

    # Component Measures 

    # strongly connected means all nodes have edges to all other nodes in the subgraph.
    num_strongly_connected = nx.number_strongly_connected_components(graph)
    print('num strongly connected components', num_strongly_connected)

    # Cover Measures

    # set of nodes s.t. each edge in the graph is incident to at least one node in said set.
    from networkx.algorithms.approximation import vertex_cover
    vertex_cover_nodes = vertex_cover.min_weighted_vertex_cover(graph)
    vertex_cover_size = len(vertex_cover_nodes)
    print('vertex cover', vertex_cover_nodes, vertex_cover_size)

    # Distance Measures

    # currently not possible b/c 
    # NetworkXError: Foundinfinte path length b/c the digraph is not strongly connected.

    # the eccentricity of a node v is the maximum distance from v to all other nodes in G
    # eccentricities = nx.eccentricity(graph)
    # eccs = [n for _, n in eccentricities.items()]
    # avg_ecc = float('%.3f'%(sum(eccs) / len(eccs)))
    # min_ecc = float('%.3f'%min(eccentricities.values()))
    # max_ecc = float('%.3f'%max(eccentricities.values()))
    # print('eccentricity', avg_ecc, min_ecc, max_ecc)

    # diameter
    # diameter = nx.diameter(graph)
    # print(diameter)

    # Shortest Path Measures

    try: 
        avg_shortest_path = nx.average_shortest_path_length(graph)
        avg_shortest_path = float('%.3f'%avg_shortest_path)
        print('avg shortest path len', avg_shortest_path)
    except: 
        avg_shortest_path = -1

    # Similarity Measures

    # this could be a fun way to compare the current graph and previous.
    # but it apparently requires scipy :(
    # if idx > 0:
    #     prev_graph = nx.read_edgelist("./pubski_data/%s.edgelist" % (idx - 1), create_using=nx.DiGraph())
    #     edit_dist = nx.graph_edit_distance(graph, prev_graph)
    #     print('edit dist', edit_dist)


    
    # ----------------------------------------------------------------------------------------------
    # 3. Write results files!
    with open("./pubski_data/results.csv", mode="a") as results_file:
        fn = ['index', 'num_nodes', 'num_edges', 'density', 'avg_degree',
                'avg_degree_central', 'min_degree_central', 'max_degree_central',
                'avg_eigen_central', 'min_eigen_central', 'max_eigen_central',
                'avg_btwn_central', 'min_btwn_central', 'max_btwn_central',
                'max_clique_size', 'clustering_coefficient', 'transitivity',
                'num_strongly_connected_components', 'vertex_cover_size', 'avg_shortest_path_len']
        results_writer = csv.DictWriter(results_file, fieldnames=fn)
        results_writer.writerow({
            'index': idx, 
            'num_nodes': num_nodes,
            'num_edges': num_edges,
            'avg_degree': avg_degree,
            'density': density, 
            'avg_degree_central': avg_degree_centrality,
            'min_degree_central': min_degree_centrality,
            'max_degree_central': max_degree_centrality,
            'avg_eigen_central': avg_ecs,
            'min_eigen_central': min_ecs,
            'max_eigen_central': max_ecs,
            'avg_btwn_central': avg_bcs,
            'min_btwn_central': min_bcs,
            'max_btwn_central': max_bcs,
            'max_clique_size': max_clique_size,
            'clustering_coefficient': clustering_coefficient,
            'transitivity': transitivity,
            'num_strongly_connected_components': num_strongly_connected,
            'vertex_cover_size': vertex_cover_size,
            'avg_shortest_path_len': avg_shortest_path
        })


