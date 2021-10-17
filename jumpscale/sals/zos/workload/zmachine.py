# from computecapacity import ComputeCapacity


from jumpscale.core.base import Base, fields
from . import Capacity, Data


class ComputeCapacity(Data):
    cpu = fields.Integer()
    memory = fields.Integer()

    @property
    def capacity(self):
        return Capacity(cru=self.cpu, mru=self.memory)


class ZNetworkInterface(Data):
    network = fields.String()
    ip = fields.String()

    # def __init__(self, network: str = "", ip: str = ""):
    #     self.network = network
    #     self.ip = ip


class ZmachineNetwork(Data):
    public_ip = fields.String()
    interfaces = fields.List(fields.Object(ZNetworkInterface))
    planetary = fields.Boolean()

    # def __init__(self, public_ip: str = "", interfaces: list = None, planetary: bool = False):
    #     self.public_ip = public_ip
    #     self.interfaces = interfaces or []
    #     self.planetary = planetary

    # def challenge(self):
    #     out = ""
    #     out += self.public_ip
    #     out += str(self.planetary)
    #     for interface in self.interfaces:
    #         out += interface.network
    #         out += interface.ip
    #     return out


class Mount(Data):
    name = fields.String()
    mountpoint = fields.String()

    # def __init__(self, name: str = "", mountpoint: str = ""):
    #     self.name = name
    #     self.mountpoint = mountpoint

    # def challenge(self):
    #     out = ""
    #     out += self.name
    #     out += self.mountpoint
    #     return out


class Zmachine(Data):
    network = fields.Object(ZmachineNetwork)
    compute_capacity = fields.Object(ComputeCapacity)
    flist = fields.String()
    entrypoint = fields.String()
    size = fields.Integer()
    mounts = fields.List(fields.Object(Mount))
    env = fields.Typed(dict)

    @property
    def capacity(self):
        return Capacity(sru=self.size)

    # def __init__(
    #     self,
    #     network: ZmachineNetwork,
    #     compute_capacity: ComputeCapacity,
    #     flist: str = "",
    #     entrypoint: str = "",
    #     size: int = 0,
    #     mounts=None,
    #     env=None,
    # ):
    #     self.flist = flist
    #     self.entrypoint = entrypoint
    #     self.network = network
    #     self.size = size
    #     self.compute_capacity = compute_capacity
    #     self.mounts = mounts or []
    #     self.env = env or {}

    # def challenge(self):
    #     out = ""
    #     out += self.flist
    #     out += self.network.challenge()
    #     out += str(self.size) if self.size else ""
    #     out += self.compute_capacity.challenge()
    #     for mount in self.mounts:
    #         out += mount.challenge()

    #     out += self.entrypoint

    #     for key in sorted(self.env):
    #         out += key
    #         out += "="
    #         out += self.env[key]
    #     return out


# response of the deployment
class ZmachineResult(Data):
    id = fields.String()
    ip = fields.IPAddress()
    # name unique per deployment, re-used in request & response
    # def _init__(self, id: str = "", ip: str = ""):
    #     self.id = id
    #     self.ip = ip
