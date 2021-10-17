import hashlib
from substrateinterface import Keypair, KeypairType
from jumpscale.core.base import Base, fields
from jumpscale.sals.zos.workload import Workload


# var md5 = require('crypto-js/md5');
# const keyring = require('@polkadot/keyring') TODO


class SignatureRequest(Base):
    twin_id = fields.Integer()
    weight = fields.Integer()
    required = fields.Boolean()

    # def __init__(self, twin_id: int, weight: int, required: bool = False):
    #     # unique id as used in TFGrid DB
    #     self.twin_id = twin_id
    #     # if put on required then this twin_id needs to sign
    #     self.required = required
    #     # signing weight
    #     self.weight = weight

    def challenge(self):
        out = ""
        out += str(self.twin_id) if self.twin_id else ""
        out += str(self.required)
        out += str(self.weight) if self.weight else ""

        return out

    # Challenge computes challenge for SignatureRequest


class Signature(Base):
    twin_id = fields.Integer()
    signature = fields.String()

    # def __init__(self, twin_id: int, signature: str):
    #     # unique id as used in TFGrid DB
    #     self.twin_id = twin_id
    #     # signature (done with private key of the twin_id)
    #     self.signature = signature


class SignatureRequirement(Base):
    weight_required = fields.Integer()
    requests = fields.List(fields.Object(SignatureRequest))
    signatures = fields.List(fields.Object(Signature), default=[])

    # def __init__(self, weight_required: int, requests: list = None, signatures: list = None):
    #     # the requests which can allow to get to required quorum
    #     self.requests = requests or []
    #     # minimal weight which needs to be achieved to let this workload become valid
    #     self.weight_required = weight_required
    #     self.signatures = signatures or []

    # Challenge computes challenge for SignatureRequest
    def challenge(self):
        out = ""
        for request in self.requests:
            out += request.challenge()

        out += str(self.weight_required) if self.weight_required else ""
        return out


# deployment is given to each Zero-OS who needs to deploy something
# the zero-os'es will only take out what is relevant for them
# if signature not done on the main Deployment one, nothing will happen
class Deployment(Base):
    version = fields.Integer()
    twin_id = fields.Integer()
    expiration = fields.Integer()
    signature_requirement = fields.Object(SignatureRequirement)
    metadata = fields.String()
    description = fields.String()
    contract_id = fields.Integer()
    workloads = fields.List(fields.Object(Workload))

    # def __init__(
    #     self,
    #     version: int,
    #     twin_id: int,
    #     expiration: int,
    #     signature_requirement: SignatureRequirement,
    #     metadata: str = "",
    #     description: str = "",
    #     contract_id: int = None,
    #     workloads: list = None,
    # ):
    #     # increments for each new interation of this model
    #     # signature needs to be achieved when version goes up
    #     self.version = version
    #     # the twin who is responsible for this deployment
    #     self.twin_id = twin_id
    #     # each deployment has unique id (in relation to originator)
    #     self.contract_id = contract_id
    #     # when the full workload will stop working
    #     # default, 0 means no expiration
    #     self.expiration = expiration
    #     self.metadata = metadata
    #     self.description = description

    #     # list of all worklaods
    #     self.workloads = workloads or []

    #     self.signature_requirement = signature_requirement

    def challenge(self):
        out = ""
        out += str(self.version) if self.version else ""
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

    def from_hex(self, s):
        string = s
        # result = bytearray(len(string) // 2)
        result = []

        for i, sub in enumerate(string[: len(string) // 2]):
            subs = string[2 * i : 2]
            if subs:
                result.append(int(string[2 * i : 2], 16))
            else:
                result.append(0)

        return result

    def to_hex(self, bs):
        encoded = []
        for sub in bs:
            encoded.append("0123456789abcdef"[(sub >> 4) & 15])
            encoded.append("0123456789abcdef"[sub & 15])

        return "".join(encoded)
        # return ""

    def sign(self, twin_id, mnemonic):
        message = self.challenge_hash()
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
