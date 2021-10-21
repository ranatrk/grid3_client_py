from jumpscale.core.base import Base, fields
from . import Data

#  is a remote wireguard client which can connect to this node
class Peer(Data):
    # is another class C in same class B as above
    subnet = fields.String()
    wireguard_public_key = fields.String()
    allowed_ips = fields.List(fields.String())
    endpoint = fields.String()


# wg network reservation (znet)
class Znet(Data):
    SKIP_CHALLENGE = ["wiregaurd_listen_port"]
    # unique nr for each network chosen, this identified private networks as connected to a container or vm or ...
    # corresponds to the 2nd number of a class B ipv4 address
    # is a class C of a chosen class B
    # form: e.g. 192.168.16.0/24
    # needs to be a private subnet
    subnet = fields.String()
    ip_range = fields.String()
    wireguard_private_key = fields.String()  # wireguard private key, curve25519
    wireguard_listen_port = fields.Integer()
    peers = fields.List(fields.Object(Peer))
