from enum import Enum
from io import StringIO
import importlib


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

    def get_value_challenge(self, value):
        if isinstance(value, dict):
            return "".join([f"{k}={v}" for k, v in sorted(value.items())])

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
    Zmachine = "zmachine"
    Zmount = "zmount"
    Znet = "network"
    Zdb = "zdb"
    Ipv4 = "ipv4"


# class WorkloadDataClasses(Enum):
#     Zmount = Zmount,
#     Zdb = Zdb,
#     Zmachine = Zmachine,
#     Znet = Znet,
#     Ipv4 = Ipv4


class Result(Base):
    pass


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


class DeploymentResultData(Base):
    pass


class DeploymentResult(Base):
    created = fields.Integer(default=0)
    state = fields.Enum(ResultStates)
    message = fields.String(default="")
    data = fields.Object(DeploymentResultData)


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
    SKIP_CHALLENGE = ["name", "id", "created", "to_delete", "result", "signature"]

    def signature(self):
        io = StringIO()
        self.challenge(io)
        challenge = io.getvalue()
        return challenge

    @classmethod
    def from_dict(cls, data):
        if isinstance(data, Workload):
            return data
        workload_obj = cls(**data)

        # Manually load data into its type eg: zmount, zmachine..etc objects
        data_type_class_name = WorkloadTypes(data["type"]).name
        data_type_module = importlib.import_module(f"jumpscale.sals.zos.workload.{data['type']}")
        data_obj = getattr(data_type_module, data_type_class_name)(**data["data"])
        workload_obj.data = data_obj
        # Manually load each data type's result
        workload_obj.result.data = getattr(data_type_module, data_type_class_name + "Result")(**data["result"]["data"])

        return workload_obj

    def data_updated(self, value):
        # update type according to workload
        self.type = WorkloadTypes[type(value).__name__].value

    # WARNING Fields order shouldn't be changed. If changed challenge will fail
    version = fields.Integer()
    name = fields.String(default="")
    type = fields.Enum(WorkloadTypes)
    metadata = fields.String(default="")
    description = fields.String(default="")
    data = fields.Object(Data, on_update=data_updated)
    result = fields.Object(DeploymentResult)
