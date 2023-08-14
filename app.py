import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
from operator import itemgetter
import os
import shutil

# Load your CSV data
df_db_int = pd.read_csv("csv/drugs_interaction_with_name.csv")

# Generate a NetworkX graph
G = nx.from_pandas_edgelist(df_db_int, 'drug_name_1', 'drug_name_2')

# Give the graph a name
G.name = 'Drug Interactions Network'

# Obtain general information of graph
num_nodes = len(G.nodes)
num_edges = len(G.edges)
avg_degree = sum(dict(G.degree).values()) / num_nodes
density = nx.density(G)

# Create dictionary to store degrees of nodes
degree_dict = dict(G.degree(G.nodes()))
nx.set_node_attributes(G, degree_dict, 'degree')

# Generate sorted list of tuples of drug entity and corresponding degree
sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)

# Create a PyVis Network object
nt = Network(notebook=False)  # Set notebook to False to render in Streamlit

# Add nodes and edges to the PyVis Network object
for node in G.nodes:
    nt.add_node(node)

for edge in G.edges:
    nt.add_edge(edge[0], edge[1])

# Save the PyVis Network object as an HTML file for the whole network
html_file = "pages/network_streamlit.html"
if os.path.exists(html_file):
    os.remove(html_file)  # Remove the file if it already exists
nt.save_graph(html_file)

# Filtrar apenas os nós relacionados ao P450
p450_nodes = [node for node in G.nodes if "P450" in node]

# Gerar um subgrafo contendo apenas os nós relacionados ao P450
G_p450 = G.subgraph(p450_nodes)

# Create a PyVis Network object for the P450 network
nt_p450 = Network(notebook=False)
for node in G_p450.nodes:
    nt_p450.add_node(node)

for edge in G_p450.edges:
    nt_p450.add_edge(edge[0], edge[1])

# Save the PyVis Network object as an HTML file for the P450 network
html_file_p450 = "pages/p450_network_streamlit.html"
if os.path.exists(html_file_p450):
    os.remove(html_file_p450)  # Remove the file if it already exists
nt_p450.save_graph(html_file_p450)

# Create a Streamlit app
def main():
    st.title("Drug Interactions Visualization")

    # Display general information about the graph
    st.write('Number of nodes:', num_nodes)
    st.write('Number of edges:', num_edges)
    st.write('Average degree:', avg_degree)
    st.write('Network density:', density)

    # Display top 20 drugs by degree
    st.write("Top 20 drugs by degree:")
    for d in sorted_degree[:20]:
        st.write(d)

    # Display the PyVis Network for the whole network in Streamlit using an iframe
    st.write("Drug Interactions Network (Whole):")
    st.components.v1.iframe(html_file, height=600)

    # Display the PyVis Network for the P450 network in Streamlit using an iframe
    st.write("P450 Drug Interactions Network:")
    st.components.v1.iframe(html_file_p450, height=600)

if __name__ == "__main__":
    main()
