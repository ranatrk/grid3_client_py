from enum import Enum


class ZdbModes(Enum):
    seq = ("seq",)
    user = "user"


class DeviceTypes(Enum):
    hdd = ("hdd",)
    ssd = "ssd"


class Zdb:
    def __init__(
        self,
        namespace: str = "",
        size: int = 0,
        mode: ZdbModes = ZdbModes.seq,
        password: str = "",
        disk_type: DeviceTypes = DeviceTypes.hdd,
        public: bool = False,
    ):
        self.namespace = namespace
        self.size = size
        self.mode = mode
        self.password = password
        self.disk_type = disk_type
        self.public = public


def challenge(self):

    out = ""
    out += self.size or ""
    out += self.mode.value
    out += self.password
    out += self.disk_type.value
    out += self.public

    return out


class ZdbResult:
    def __init__(self, name: str = "", namespace: str = "", ips: list = None, port: int = 0):
        self.name = name
        self.namespace = namespace
        self.ips = ips or []
        self.port = port


# export { Zdb, ZdbResult }
