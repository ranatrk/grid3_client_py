from .computecapacity import ComputeCapacity


class ZNetworkInterface:
    network: str
    ip: str

    def __init__(self, network: str = "", ip: str = ""):
        self.network = network
        self.ip = ip


class ZmachineNetwork:
    def __init__(self, public_ip: str = "", interfaces: list = None, planetary: bool = False):
        self.public_ip = public_ip
        self.interfaces = interfaces or []
        self.planetary = planetary

    def challenge(self):
        out = ""
        out += self.public_ip
        out += str(self.planetary)
        for interface in self.interfaces:
            out += interface.network
            out += interface.ip
        return out


class Mount:
    name: str
    mountpoint: str

    def __init__(self, name: str = "", mountpoint: str = ""):
        self.name = name
        self.mountpoint = mountpoint

    def challenge(self):
        out = ""
        out += self.name
        out += self.mountpoint
        return out


class Zmachine():
    def __init__(self,network: ZmachineNetwork, compute_capacity: ComputeCapacity,flist: str = "",entrypoint: str = "", , size: int=0, mounts= None,env = None):
        self.flist = flist
        self.entrypoint = entrypoint
        self.network = network
        self.size = size
        self.compute_capacity = compute_capacity
        self.mounts = mounts or []
        self.env = env or {}

    def challenge(self):
        out = ""
        out += self.flist
        out += self.network.challenge()
        out += str(self.size) if self.size else ""
        out += self.compute_capacity.challenge()
        for mount in self.mounts{
			out += mount.challenge();
		}
        out += self.entrypoint
        
        for key in sorted(self.env):
            out += key
            out += "="
            out += self.env[key]
        return out



# response of the deployment
class ZmachineResult():
	# name unique per deployment, re-used in request & response
    def _init__(self,id:str="",ip:str=""):
        self.id = id
        self.ip = ip




