class IPNode:
    def __init__(self, ip: str, prefix: str):
        self.ip = ip
        self.prefix = prefix
    def __eq__(self, other) -> bool:
        if not isinstance(other, IPNode):
            return False
        return self.ip == other.ip and self.prefix == other.prefix
    def __str__(self) -> str:
        return self.ip