from enum import Enum

from .ipv4 import PublicIP
from .zdb import Zdb, ZdbResult
from .zmachine import Zmachine, ZmachineResult
from .zmount import Zmount, ZmountResult
from .znet import Znet


class ResultStates(Enum):
    error = ("error",)
    ok = ("ok",)
    deleted = "deleted"


class WorkloadTypes(Enum):
    zmachine = ("zmachine",)
    zmount = ("zmount",)
    network = ("network",)
    zdb = ("zdb",)
    ipv4 = "ipv4"


class WorkloadData(Enum):
    Zmount,
    Zdb,
    Zmachine,
    Znet


class WorkloadDataResult(Enum):
    ZmountResult,
    ZdbResult,
    ZmachineResult


# class Right(Enum):
# 	restart,
# 	delete,
# 	stats,
# 	logs


# Access Control Entry
class ACE:
    # the administrator twin id
    # twin_ids: number[];
    # rights: Right[];
    def __init__(self, twin_ids: list = None, rights: list = None):
        self.twin_ids = twin_ids or []
        self.rights = rights or []


class DeploymentResult:
    def __init__(self, created: int = 0, state: ResultStates = None, error: str = "", data: str = ""):
        self.created = created
        self.state = state
        self.error = error
        self.data = data  # also json.RawMessage


class Workload:
    def __init__(
        self,
        version: int,
        name: str,
        type: WorkloadTypes,
        data: Zmount or Znet or Zmachine or Zdb or PublicIP,
        metadata: str,
        description: str,
        result: DeploymentResult,
    ):
        self.version = version
        # unique name per Deployment
        self.name = name
        self.type = type
        # this should be something like json.RawMessage in golang
        self.data = data  # serialize({size: 10}) ---> "data": {size:10},
        self.metadata = metadata
        self.description = description
        # list of Access Control Entries
        # what can an administrator do
        # not implemented in zos
        # acl []ACE
        self.result = result

    def challenge(self):
        out = ""
        out += str(self.version)
        out += self.type.value
        out += self.metadata
        out += self.description
        out += self.data.challenge()
        return out

