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
    SKIP_CHALLENGE = ["namespace", "disk_type"]
    # WARNING Fields order shouldn't be changed. If changed challenge will fail
    namespace = fields.String(default="")
    size = fields.Integer()
    mode = fields.Enum(ZdbModes)
    password = fields.String(default="")
    disk_type = fields.Enum(DeviceTypes)
    public = fields.Boolean()

    @property
    def capacity(self):
        if self.disk_type == DeviceType.HDD:
            return Capacity(hru=self.size)
        else:
            return Capacity(sru=self.size)


class ZdbResult(Data):
    name = fields.String(default="")
    namespace = fields.String(default="")
    ips = fields.List(fields.IPAddress())
    port = fields.Integer()
