from enum import Enum
from io import StringIO

# from typing import List, Union

# from workload.ipv4 import PublicIP
# from workload.zdb import Zdb, ZdbResult
# from workload.zmachine import Zmachine, ZmachineResult
# from workload.zmount import Zmount, ZmountResult
# from workload.znet import Znet


from jumpscale.core.base import Base, fields


class Challengeable(Base):
    """
    a base type to build challenges from fields
    ordering of field definition is a mandatory, to exclude any field from
    the challenge string, just add its name to `SKIP_CHALLENGE` list.
    """

    # field names to be excluded from the challenge string
    SKIP_CHALLENGE = []

    def is_challengeable(self, value_or_type):
        if isinstance(value_or_type, type):
            return issubclass(value_or_type, Challengeable)
        return isinstance(value_or_type, Challengeable)

        # def get_value_challenge(self, value):
        #     if isinstance(value, dict):
        #         return "".join([f"{k}={v}" for k, v in sorted(value.items())])

        if isinstance(value, (list, tuple, set)):
            return "".join(map(str, value))

        if isinstance(value, bool):
            return str(value).lower()

        return str(value)

    def challenge(self, io):
        all_fields = self._get_fields()

        for name, field in all_fields.items():
            if name in self.SKIP_CHALLENGE:
                continue

            value = getattr(self, name)
            if self.is_challengeable(value):
                value.challenge(io)
                continue

            if isinstance(field, fields.List):
                if isinstance(field.field, fields.Object):
                    if self.is_challengeable(field.field.type):
                        for obj in value:
                            obj.challenge(io)
                        continue

            # write raw value to io
            raw_value = field.to_raw(value)
            io.write(self.get_value_challenge(raw_value))


class ResultStates(Enum):
    error = "error"
    ok = "ok"
    deleted = "deleted"


class WorkloadTypes(Enum):
    zmachine = "zmachine"
    zmount = "zmount"
    network = "network"
    zdb = "zdb"
    ipv4 = "ipv4"


# class WorkloadData(Enum):
#     Zmount,
#     Zdb,
#     Zmachine,
#     Znet


class Result(Base):
    pass


# class WorkloadDataResult(Enum):
#     ZmountResult,
#     ZdbResult,
#     ZmachineResult


class Right(Enum):
    restart = "restart"
    delete = "delete"
    stats = "stats"
    logs = "logs"


class DeviceType(Enum):
    HDD = "hdd"
    SSD = "ssd"


# Access Control Entry
class ACE(Base):
    twin_ids = fields.List(fields.Integer())
    rights = fields.List(fields.Enum(Right))
    # the administrator twin id
    # twin_ids: number[];
    # rights: Right[];
    # def __init__(self, twin_ids: list = None, rights: list = None):
    #     self.twin_ids = twin_ids or []
    #     self.rights = rights or []


class DeploymentResult(Base):
    created = fields.Integer()
    state = fields.Object(ResultStates)
    error = fields.String()
    data = fields.String()

    # def __init__(self, created: int = 0, state: ResultStates = None, error: str = "", data: str = ""):
    #     self.created = created
    #     self.state = state
    #     self.error = error
    #     self.data = data  # also json.RawMessage


class Capacity(Base):
    cru = fields.Integer()
    sru = fields.Integer()
    hru = fields.Integer()
    mru = fields.Integer()
    ipv4u = fields.Integer()


class Data(Challengeable):
    @property
    def capacity(self):
        return Capacity()


class Workload(Challengeable):
    SKIP_CHALLENGE = ["id", "created", "to_delete", "result", "signature"]

    def signature(self):
        io = StringIO()
        self.challenge(io)
        challenge = io.getvalue()
        # should return hex(ed25519.sign(sk, challenge)
        # sk => identity secret
        return challenge

    def data_updated(self, value):
        # update type according to workload
        self.type = WorkloadTypes[type(value).__name__].value

    version = fields.Integer()
    name = fields.String()
    type = fields.Enum(WorkloadTypes)
    data = fields.Object(Data, on_update=data_updated)
    # data = Union[Zmount, Znet, Zmachine, Zdb, PublicIP] # FIXME TODO
    metadata = fields.String()
    description = fields.String()
    # result = fields.Object(DeploymentResult)

    # id = fields.String()
    # created = fields.DateTime()
    # to_delete = fields.Boolean()
    # signature = fields.String(compute=get_signature)
    result = fields.Object(Result)
