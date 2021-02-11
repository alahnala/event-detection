import networkx as nx
import community
import matplotlib.pyplot as plt
import sys
from collections import defaultdict


def construct_graph(graph_file):
	'''
	returns graph and node to phrase map
	'''
	with open(graph_file) as f:
		lines = f.readlines()
	G = nx.Graph() #define the graph 

	phrase_to_node = {} #maps phrase to number indicating the node
	for line in lines:
		phrases = line.split('\t')[:2]
		edge_weight = float(line.split('\t')[2])
		
		if phrases[0] in phrase_to_node:
			#do not need to create a new node
			node1 = phrase_to_node[phrases[0]]
		else:
			phrase_to_node[phrases[0]] = len(phrase_to_node)
			node1 = phrase_to_node[phrases[0]]
			#create a new node
			G.add_node(node1)
			G.nodes[node1]['phrase'] = phrases[0]
		if phrases[1] in phrase_to_node:
			#do not need to create a new node
			node2 = phrase_to_node[phrases[1]]
		else:
			phrase_to_node[phrases[1]] = len(phrase_to_node)
			node2 = phrase_to_node[phrases[1]]
			#create a new node
			G.add_node(node2)
			G.nodes[node2]['phrase'] = phrases[1]
		#the phrases in the set become nodes and the jaccard coefficient become the node weights
		G.add_edge(node1, node2, weight=edge_weight) #add weighted edge
	return G

def louvain(G):
	'''
	Input graph G. 
	'''

	# partition is a dictionary that maps node to its community.
	partition = community.best_partition(G, weight='weight') 
	return partition

def community_to_nodes(partition):
	'''
	input partition is a dictionary that maps node to its community.
	'''
	community_map = defaultdict(lambda:[])
	nodes = partition.keys()
	for node in nodes:
		community = partition[node]
		community_map[community].append(node)

	return community_map

def community_to_phrases(communities, G):
	'''
	input partition is a dictionary that maps node to its community.
	'''
	community_map = defaultdict(lambda:[])
	for c in communities:
		nodes = communities[c]
		for node in nodes:
			community_map[c].append(G.nodes[node]['phrase'])

	return community_map

def get_event_candidates(graph_file):
	G = construct_graph(graph_file)
	partition = louvain(G)
	communities = community_to_nodes(partition)
	event_candidates = community_to_phrases(communities, G)
	return event_candidates


def main():

	graph_file = sys.argv[1]
	G = construct_graph(graph_file)
	partition = louvain(G)
	communities = community_to_nodes(partition)
	event_candidates = community_to_phrases(communities, G) #there are the event candidates at the timestep indicated by the file.
	# print(event_candidates)
	# phrase_clusters(partition)


if __name__ == "__main__":
	main()