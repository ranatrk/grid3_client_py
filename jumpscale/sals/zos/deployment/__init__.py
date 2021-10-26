import hashlib
from io import StringIO
from substrateinterface import Keypair, KeypairType
from jumpscale.core.base import Base, fields, meta

from jumpscale.sals.zos.workload import Workload, WorkloadTypes
from .workloads import Workloads


# var md5 = require('crypto-js/md5');
# const keyring = require('@polkadot/keyring') TODO


class SignatureRequest(Base):
    twin_id = fields.Integer()
    required = fields.Boolean()
    weight = fields.Integer()

    def challenge(self):
        out = ""
        out += str(self.twin_id) if self.twin_id else ""
        out += str(self.required).lower()
        out += str(self.weight) if self.weight else ""

        return out


class Signature(Base):
    twin_id = fields.Integer()
    signature = fields.String(default="")


class SignatureRequirement(Base):
    SKIP_CHALLENGE = ["signatures"]

    requests = fields.List(fields.Object(SignatureRequest))
    weight_required = fields.Integer()
    signatures = fields.List(fields.Object(Signature), default=[])

    # # Challenge computes challenge for SignatureRequest
    def challenge(self):
        out = ""
        for request in self.requests:
            out += request.challenge()

        out += str(self.weight_required) if self.weight_required else ""
        return out


class WorkloadsField(fields.Typed):
    def __init__(self):
        super().__init__(type_=Workloads, default=lambda: Workloads())

    def from_raw(self, raw):
        loads = Workloads()
        for item in raw:
            w = Workload.from_dict(item)
            loads.append(w)

        return loads

    def to_raw(self, loads):
        return [w.to_dict() for w in loads]

    def _get_data(self):
        # ovverride _get_data from Base to have the data in the form of list of workloads instead of dict of list of workloads
        # initial {'workloads':[]}  -> to be returned as {}
        workloads = super(Workloads, self)._get_data()

    to_dict = _get_data


# deployment is given to each Zero-OS who needs to deploy something
# the zero-os'es will only take out what is relevant for them
# if signature not done on the main Deployment one, nothing will happen
class Deployment(Base):
    # SKIP_CHALLENGE = ["name", "contract_id"]

    version = fields.Integer()
    twin_id = fields.Integer()
    metadata = fields.String(default="")
    description = fields.String(default="")
    expiration = fields.Integer()
    workloads = WorkloadsField()
    signature_requirement = fields.Object(SignatureRequirement)
    contract_id = fields.Integer()

    # def signature(self):
    #     io = StringIO()
    #     self.challenge(io)
    #     challenge = io.getvalue()
    #     # should return hex(ed25519.sign(sk, challenge)
    #     # sk => identity secret
    #     return challenge

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def challenge(self):
        out = ""
        out += str(self.version) if self.version else "0"
        out += str(self.twin_id) if self.twin_id else ""
        out += str(self.metadata)
        out += str(self.description)
        out += str(self.expiration) if self.expiration else ""
        for workload in self.workloads:
            out += workload.signature()

        out += self.signature_requirement.challenge()
        return out

    # ChallengeHash computes the hash of the challenge signed
    # by the user. used for validation
    def challenge_hash(self):
        return hashlib.md5(self.challenge().encode()).hexdigest()

    def sign(self, twin_id, mnemonic):
        message = "0x" + self.challenge_hash()
        # message_bytes = self.from_hex(message)

        # keyr = keyring.Keyring({ type: 'ed25519' }) # TODO
        # key = keyr.addFromMnemonic(mnemonic)
        # signed_msg = key.sign(message_bytes)

        keypair = Keypair.create_from_mnemonic(mnemonic, crypto_type=KeypairType.ED25519)

        signed_msg = keypair.sign(message)[2:]
        # hex_signed_msg = self.to_hex(signed_msg)
        for sig in self.signature_requirement.signatures:
            if sig.twin_id == twin_id:
                sig.signature = signed_msg
        signature = Signature(twin_id=twin_id, signature=signed_msg)
        # signature.twin_id = twin_id
        # signature.signature = signed_msg
        self.signature_requirement.signatures.append(signature)
