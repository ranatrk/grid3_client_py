#  ssd mounts under zmachine

#  ONLY possible on SSD
from jumpscale.core.base import Base, fields
from . import Capacity, Data, DeploymentResultData


class Zmount(Data):
    # WARNING Fields order shouldn't be changed. If changed challenge will fail
    size = fields.Integer()

    @property
    def capacity(self):

        return Capacity(sru=self.size)


class ZmountResult(DeploymentResultData):
    # WARNING Fields order shouldn't be changed. If changed challenge will fail
    volume_id = fields.String(default="")
