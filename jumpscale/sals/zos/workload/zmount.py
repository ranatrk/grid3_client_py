#  ssd mounts under zmachine

#  ONLY possible on SSD
from jumpscale.core.base import Base, fields
from . import Capacity, Data


class Zmount(Data):
    size = fields.Integer()

    @property
    def capacity(self):

        return Capacity(sru=self.size)


class ZmountResult(Data):
    volume_id = fields.String(default="")
