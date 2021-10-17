from enum import Enum

from jumpscale.core.base import Base, fields
from . import Capacity, DeviceType, Data


class ZdbModes(Enum):
    seq = "seq"
    user = "user"


class DeviceTypes(Enum):
    hdd = "hdd"
    ssd = "ssd"


class Zdb(Data):
    namespace = fields.String()
    size = fields.Integer()
    mode = fields.Enum(ZdbModes)
    password = fields.String()
    disk_type = fields.Enum(DeviceTypes)
    public = fields.Boolean()

    # def __init__(
    #     self,
    #     namespace: str = "",
    #     size: int = 0,
    #     mode: ZdbModes = ZdbModes.seq,
    #     password: str = "",
    #     disk_type: DeviceTypes = DeviceTypes.hdd,
    #     public: bool = False,
    # ):
    #     self.namespace = namespace
    #     self.size = size
    #     self.mode = mode
    #     self.password = password
    #     self.disk_type = disk_type
    #     self.public = public
    @property
    def capacity(self):
        if self.disk_type == DeviceType.HDD:
            return Capacity(hru=self.size)
        else:
            return Capacity(sru=self.size)


# def challenge(self):

#     out = ""
#     out += self.size or ""
#     out += self.mode.value
#     out += self.password
#     out += self.disk_type.value
#     out += self.public

#     return out


class ZdbResult(Data):
    name = fields.String()
    namespace = fields.String()
    ips = fields.List(fields.IPAddress())
    port = fields.Integer()

    # def __init__(self, name: str = "", namespace: str = "", ips: list = None, port: int = 0):
    #     self.name = name
    #     self.namespace = namespace
    #     self.ips = ips or []
    #     self.port = port
