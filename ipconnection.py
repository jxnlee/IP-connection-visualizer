from ipnode import IPNode

class IPConnection:
    successful_conn_states = ['S1', 'SF', 'S3', 'RSTRH', 'SHR']
    unsuccessful_conn_states = ['REJ', 'S0', 'S2', 'RSTR', 'RSTOS0', 'SH', 'OTH']

    def __init__(self, src: IPNode, dest: IPNode, conn_state: str, orig_bytes: int):
        self.src = src
        self.dest = dest
        self.conn_state = conn_state
        self.orig_bytes = orig_bytes
        self.is_successful = IPConnection.get_conn_status(self.conn_state, self.orig_bytes)
        self.ports = []
    
    @staticmethod
    def get_conn_status(state: str, orig_bytes: int) -> bool:
        if state in IPConnection.successful_conn_states:
            return True
        elif state in IPConnection.unsuccessful_conn_states:
            return False
        elif state == 'RSTO':
            return orig_bytes > 0
        else:
            return False
    
    def add_port(self, src_port: str, dest_port: str):
        self.ports.append((src_port, dest_port))

    def get_label(self) -> str:
        unique_dest_ports = set(x[1] for x in self.ports)
        num_dest_ports = len(unique_dest_ports)
        label = ''
        for count, port in enumerate(unique_dest_ports):
            if count > 0:
                label += ', '
            if count == 5:
                label += '...'
                break
            label += port

        label += f' ({str(num_dest_ports)})'
        return label

    def __eq__(self, other) -> bool:
        if not isinstance(other, IPConnection):
            return False
        return self.src == other.src and self.dest == other.dest and self.is_successful == other.is_successful