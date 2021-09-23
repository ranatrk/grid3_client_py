class ComputeCapacity:
    def __init__(self, cpu: int, memory: int):
        # cpu cores, minimal 10 cpu_centi_core
        # always reserved with overprovisioning of about 1/4-1/6

        # memory in bytes, minimal 100 MB
        # always reserved

        # min disk size reserved (to make sure you have growth potential)
        # when reserved it means you payment
        # if you use more, you pay for it
        self.cpu = cpu
        self.memory = memory

    def challenge(self):
        out = ""
        out += str(self.cpu) if self.cpu else ""
        out += str(self.memory) if self.memory else ""
        return out

