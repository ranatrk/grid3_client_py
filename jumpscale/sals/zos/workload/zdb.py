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

    @property
    def capacity(self):
        if self.disk_type == DeviceType.HDD:
            return Capacity(hru=self.size)
        else:
            return Capacity(sru=self.size)


class ZdbResult(Data):
    name = fields.String()
    namespace = fields.String()
    ips = fields.List(fields.IPAddress())
    port = fields.Integer()
