# import libraries to be used
import pandas as pd
from pyvis.network import Network
import webbrowser
from ipnode import IPNode
from ipconnection import IPConnection

class Visualizer:

    # list of relevant properties to consider in our data
    relevant_properties = {
        'src ip': 'synth_src_ip',
        'dest ip': 'synth_dest_ip',
        'conn state': 'conn_state',
        'orig bytes': 'orig_bytes',
        'src port': 'src_port',
        'dest port': 'dest_port',
        'src prefix': 'prefix_src',
        'dest prefix': 'prefix_dest'
        }
    src_ip_prop = relevant_properties['src ip']
    dest_ip_prop = relevant_properties['dest ip']
    conn_state_prop = relevant_properties['conn state']
    orig_bytes_prop = relevant_properties['orig bytes']
    src_port_prop = relevant_properties['src port']
    dest_port_prop = relevant_properties['dest port']
    src_prefix_prop = relevant_properties['src prefix']
    dest_prefix_prop = relevant_properties['dest prefix']

    prefix_colors = [
        'brown',
        'wheat',
        'orange',
        'salmon',
        'yellow',
        'goldenrod',
        'blue',
        'cyan',
        'purple',
        'indigo',
        'pink',
        'magenta'
    ]
    

    # categorizations of connection states
    successful_connection_states = ['S1', 'SF', 'S3', 'RSTRH', 'SHR']
    unsuccessful_connection_states = ['REJ', 'S0', 'S2', 'RSTR', 'RSTOS0', 'SH', 'OTH']
    
    def __init__(self, input_file_path, output_file_path, template_file_path='template.html.j2', successful_conn_color='green', unsuccessful_conn_color='red'):
        # input and output file paths
        self.input_file = input_file_path
        self.output_file = output_file_path
        self.template_file = template_file_path

        # connect state colors
        self.successful_color = successful_conn_color
        self.unsuccessful_color = unsuccessful_conn_color

        self.nodes = {}
        self.edges = {}

    def populate_graph(self):
        self.init_df = pd.read_csv(self.input_file)
        self.df = self.init_df[list(Visualizer.relevant_properties.values())]

        self.prefix_colors_dict = dict(zip(pd.concat([self.df[Visualizer.src_prefix_prop], self.df[Visualizer.dest_prefix_prop]]).unique().tolist(), Visualizer.prefix_colors))

        for index, row in self.df.iterrows():
            src_ip = str(row[Visualizer.src_ip_prop])
            dest_ip = str(row[Visualizer.dest_ip_prop])
            src_port = str(row[Visualizer.src_port_prop])
            dest_port = str(row[Visualizer.dest_port_prop])
            src_prefix = str(row[Visualizer.src_prefix_prop])
            dest_prefix = str(row[Visualizer.dest_prefix_prop])
            state = str(row[Visualizer.conn_state_prop])
            try: 
                orig_bytes = int(row[Visualizer.orig_bytes_prop])
            except:
                orig_bytes = 0

            if src_ip not in self.nodes:
                self.nodes[src_ip] = IPNode(src_ip, src_prefix)
            if dest_ip not in self.nodes:
                self.nodes[dest_ip] = IPNode(dest_ip, dest_prefix)
            
            src_node = self.nodes[src_ip]
            dest_node = self.nodes[dest_ip]

            edge_tuple = (src_ip, dest_ip, IPConnection.get_conn_status(state, orig_bytes))
            if edge_tuple not in self.edges:
                self.edges[edge_tuple] = IPConnection(src_node, dest_node, state, orig_bytes)
            
            self.edges[edge_tuple].add_port(src_port, dest_port)
    
    def generate_visual(self):
        # generate the graph visual and save the file to our output file path
        self.graph_visual = Network(cdn_resources='local', directed=True, select_menu=True, filter_menu=True)
        #self.graph_visual.set_template(path_to_template=self.template_file)
        # self.graph_visual.show_buttons(filter_=['physics'])
        self.graph_visual.force_atlas_2based()

        for ip in self.nodes:
            self.graph_visual.add_node(ip, color=self.prefix_colors_dict[self.nodes[ip].prefix])
        for edge in self.edges:
            self.graph_visual.add_edge(edge[0], edge[1], color=self.successful_color if self.edges[edge].is_successful else self.unsuccessful_color, label=self.edges[edge].get_label())
        self.graph_visual.save_graph(self.output_file)
    
    '''
    def populate_graph(self):
        # make a dataframe from our csv file and filter out irrelevant properties
        self.init_df = pd.read_csv(self.input_file)
        self.df = self.init_df[list(Visualizer.relevant_properties.values())]

        # generate list of nodes and edges in our graph (assigning edges to their corresponding colors)
        self.nodes = pd.concat([self.df[Visualizer.src_ip_prop], self.df[Visualizer.dest_ip_prop]]).unique().tolist()
        for index, row in self.df.iterrows():
            edge_tuple = (row[self.src_ip_prop], row[self.dest_ip_prop])
            edge_label = str(row[self.src_port_prop]) + "_" + str(row[self.dest_port_prop])
            state = row[self.conn_state_prop]

            if(state in self.successful_connection_states and edge_tuple not in self.successful_edges):
                self.successful_edges[edge_tuple] = edge_label
            elif(state in self.unsuccessful_connection_states and edge_tuple not in  self.unsuccessful_edges):
                self.unsuccessful_edges[edge_tuple] = edge_label
            elif(state == 'RSTO'):
                if(int(row[self.orig_bytes_prop]) > 0 and edge_tuple not in self.successful_edges):
                    self.successful_edges[edge_tuple] = edge_label
                elif(int(row[self.orig_bytes_prop]) == 0 and edge_tuple not in self.unsuccessful_edges):
                    self.unsuccessful_edges[edge_tuple] = edge_label
    
    def generate_visual(self):
        # generate the graph visual and save the file to our output file path
        self.graph_visual = Network(cdn_resources='local', directed=True, select_menu=True, filter_menu=True)
        #self.graph_visual.set_template(path_to_template=self.template_file)
        self.graph_visual.show_buttons(filter_=['physics'])
        self.graph_visual.add_nodes(self.nodes)
        for successful_edge in self.successful_edges:
            self.graph_visual.add_edge(successful_edge[0], successful_edge[1], color=self.successful_color, label=self.successful_edges[successful_edge])
        for unsuccessful_edge in self.unsuccessful_edges:
            self.graph_visual.add_edge(unsuccessful_edge[0], unsuccessful_edge[1], color=self.unsuccessful_color, label=self.unsuccessful_edges[unsuccessful_edge])
        self.graph_visual.save_graph(self.output_file)
    '''
    def load_visual_new_tab(self):
        webbrowser.open_new_tab(self.output_file)

def main():
    connection_visual = Visualizer(input_file_path='synthetic_data_PREFIX.csv', output_file_path='connection_visual.html')
    connection_visual.populate_graph()
    connection_visual.generate_visual()
    connection_visual.load_visual_new_tab()


if __name__ == '__main__':
    main()