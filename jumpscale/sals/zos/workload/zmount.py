#  ssd mounts under zmachine

#  ONLY possible on SSD
from jumpscale.core.base import Base, fields
from . import Capacity, Data


class Zmount(Data):
    size = fields.Integer()

    # def __init__(self, size):
    #     self.size = size

    # def challenge(self):
    #     out = str(self.size) if self.size else ""
    #     return out

    @property
    def capacity(self):

        return Capacity(sru=self.size)


class ZmountResult(Data):
    volume_id = fields.String()

    # def __init__(self, volume_id: str = ""):
    #     self.volume_id = volume_id
