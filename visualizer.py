# import libraries to be used
import pandas as pd
from pyvis.network import Network
import webbrowser

# input and output file paths
input_data_file_path = 'synthetic_data.csv'
output_html_file_path = 'connection_visual.html'

# list of relevant properties to consider in our data
relevant_properties = ['synth_src_ip', 'synth_dest_ip', 'conn_state', 'orig_bytes']

# categorizations of connection states
successful_connection_states = ['S1', 'SF', 'S3', 'RSTRH', 'SHR']
unsuccessful_connection_states = ['REJ', 'S0', 'S2', 'RSTR', 'RSTOS0', 'SH', 'OTH']

# make a dataframe from our csv file and filter out irrelevant properties
df = pd.read_csv(input_data_file_path)
df_relevant = df[relevant_properties]

# generate list of nodes and edges in our graph (assigning edges to their corresponding colors)
nodes = pd.concat([df_relevant['synth_src_ip'], df_relevant['synth_dest_ip']]).unique().tolist()
red_edges = []
green_edges = []
for index, row in df_relevant.iterrows():
    edge_tuple = (row['synth_src_ip'], row['synth_dest_ip'])
    state = row['conn_state']
    if(state in successful_connection_states and edge_tuple not in green_edges):
        green_edges.append(edge_tuple)
    elif(state in unsuccessful_connection_states and edge_tuple not in  red_edges):
        red_edges.append(edge_tuple)
    elif(state == 'RSTO'):
        if(int(row['orig_bytes']) > 0 and edge_tuple not in green_edges):
            green_edges.append(edge_tuple)
        elif(int(row['orig_bytes']) == 0 and edge_tuple not in red_edges):
            red_edges.append(edge_tuple)

# generate the graph visual and save the file to our output file path
graph_visual = Network(notebook=True, cdn_resources='remote', directed=True)
graph_visual.show_buttons(filter_=['physics'])
graph_visual.add_nodes(nodes)
for green_edge in green_edges:
    graph_visual.add_edge(green_edge[0], green_edge[1], color='green')
for red_edge in red_edges:
    graph_visual.add_edge(red_edge[0], red_edge[1], color='red')
graph_visual.save_graph(output_html_file_path)

# open the output html file in a new browser tab
webbrowser.open_new_tab(output_html_file_path)