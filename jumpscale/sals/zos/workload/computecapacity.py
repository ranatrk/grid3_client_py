from jumpscale.core.base import Base, fields
from . import Capacity, Data


class ComputeCapacity(Data):
    cpu = fields.Integer()
    memory = fields.Integer()

    # cpu cores, minimal 10 cpu_centi_core
    # always reserved with overprovisioning of about 1/4-1/6

    # memory in bytes, minimal 100 MB
    # always reserved

    # min disk size reserved (to make sure you have growth potential)
    # when reserved it means you payment
    # if you use more, you pay for it

    @property
    def capacity(self):
        return Capacity(cru=self.cpu, mru=self.memory)
