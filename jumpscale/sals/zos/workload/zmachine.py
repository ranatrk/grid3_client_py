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
    network = fields.String(default="")
    ip = fields.String(default="")


class ZmachineNetwork(Data):
    public_ip = fields.String(default="")
    planetary = fields.Boolean()
    interfaces = fields.List(fields.Object(ZNetworkInterface))


class Mount(Data):
    name = fields.String(default="")
    mountpoint = fields.String(default="")


class Zmachine(Data):
    flist = fields.String(default="")
    network = fields.Object(ZmachineNetwork)
    size = fields.Integer()
    compute_capacity = fields.Object(ComputeCapacity)
    mounts = fields.List(fields.Object(Mount))
    entrypoint = fields.String(default="")
    env = fields.Typed(dict)

    @property
    def capacity(self):
        return Capacity(sru=self.size)


# response of the deployment
class ZmachineResult(Data):
    id = fields.String(default="")
    ip = fields.IPAddress()
    # name unique per deployment, re-used in request & response
