#  ssd mounts under zmachine

#  ONLY possible on SSD
class Zmount:
    def __init__(self, size: bytes):
        self.size = size

    def challenge(self):
        out = str(self.size) if self.size else ""
        return out


class ZmountResult:
    def __init__(self, volume_id: str = ""):
        self.volume_id = volume_id

