# from computecapacity import ComputeCapacity


from jumpscale.core.base import Base, fields
from . import Capacity, Data, DeploymentResultData


class ComputeCapacity(Data):
    # WARNING Fields order shouldn't be changed. If changed challenge will fail
    cpu = fields.Integer()
    memory = fields.Integer()

    @property
    def capacity(self):
        return Capacity(cru=self.cpu, mru=self.memory)


class ZNetworkInterface(Data):
    # WARNING Fields order shouldn't be changed. If changed challenge will fail
    network = fields.String(default="")
    ip = fields.String(default="")


class ZmachineNetwork(Data):
    # WARNING Fields order shouldn't be changed. If changed challenge will fail
    public_ip = fields.String(default="")
    planetary = fields.Boolean()
    interfaces = fields.List(fields.Object(ZNetworkInterface))


class Mount(Data):
    # WARNING Fields order shouldn't be changed. If changed challenge will fail
    name = fields.String(default="")
    mountpoint = fields.String(default="")


class Zmachine(Data):
    # WARNING Fields order shouldn't be changed. If changed challenge will fail
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


class ZmachineResult(DeploymentResultData):
    # WARNING Fields order shouldn't be changed. If changed challenge will fail
    id = fields.String(default="")
    ip = fields.IPAddress()
    ygg_ip = fields.String(default="")
    # name unique per deployment, re-used in request & response
