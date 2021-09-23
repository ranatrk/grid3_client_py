#  is a remote wireguard client which can connect to this node
class Peer:
    # is another class C in same class B as above
    subnet: str
    wireguard_public_key: str
    allowed_ips: list
    endpoint: str

    def __init__(self, subnet: str = "", wireguard_public_key: str = "", allowed_ips: list = None, endpoint: str = ""):
        self.subnet = subnet
        # wireguard public key, curve25519
        self.wireguard_public_key = wireguard_public_key
        self.allowed_ips = allowed_ips or []
        # ipv4 or ipv6
        # can be empty, one of the 2 need to be filled in though
        self.endpoint = endpoint

    def challenge(self):
        out = ""
        out += self.wireguard_public_key
        out += self.endpoint
        out += self.subnet
        for ip in self.allowed_ips:
            out += ip
        return out


# wg network reservation (znet)
class Znet():
    # unique nr for each network chosen, this identified private networks as connected to a container or vm or ...
    # corresponds to the 2nd number of a class B ipv4 address
    # is a class C of a chosen class B
    # form: e.g. 192.168.16.0/24
    # needs to be a private subnet
    subnet: str
    ip_range: str
    # wireguard private key, curve25519
    wireguard_private_key: str
    # >1024?
    wireguard_listen_port: int
    peers: list
    
    def __init__(self,subnet: str = "", ip_range: str = "", wireguard_private_key: str = "", wireguard_listen_port: int, peers: list=None):
        self.subnet = subnet
        self.ip_range = ip_range
        self.wireguard_private_key = wireguard_private_key
        self.wireguard_listen_port = wireguard_listen_port
        self.peers = peers or []
    
    def challenge(self):
        out = ""
        out += self.ip_range
        out += self.subnet
        out += self.wireguard_private_key
        out += str(self.wireguard_listen_port) if self.wireguard_listen_port else ""
        for peer in self.peers:
            out += peer.challenge()
        return out

