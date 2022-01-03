import os
from enum import Enum
from substrateinterface import Keypair, KeypairType, SubstrateInterface
from .twin import Twin
from .farm import Farm
from .contract import Contract
from .entity import Entity

from jumpscale.clients.base import Client
from jumpscale.core.base import fields
from jumpscale.loader import j

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
TYPES_PATH = f"{BASE_PATH}/types.json"  # TODO fix path
SUBSTRATE_URL = "wss://tfchain.dev.grid.tf/ws"


class KeypairTypeEnum(Enum):
    SR25519 = KeypairType.SR25519
    ED25519 = KeypairType.ED25519


class TfgridClient(Client):
    def reset_keypair(self, value=None):
        self._keypair = None

    def reset_interface(self, value=None):
        self._keypair = None

    url = fields.String(required=True, allow_empty=False, on_update=reset_interface)
    words = fields.Secret(required=True, allow_empty=False, on_update=reset_keypair)
    type_registry = fields.Typed(dict)
    crypto_type = fields.Enum(KeypairTypeEnum)
    # keypair = fields.Typed(Keypair)
    # interface = fields.Typed(SubstrateInterface)

    def __init__(self, url="", words="", type_registry=None, crypto_type="SR25519", **kwargs):
        super().__init__(
            url=url, words=words, type_registry=type_registry, crypto_type=KeypairTypeEnum[crypto_type], **kwargs
        )
        self.url = url or SUBSTRATE_URL
        self.words = words or self.generatMnemonic()
        self._keypair = Keypair.create_from_mnemonic(self.words, crypto_type=self.crypto_type.value)  # FIXME

        self.type_registry = type_registry or j.data.serializers.json.load_from_file(TYPES_PATH)
        self._interface = None

        self.twin = Twin(self.interface, self.keypair)
        self.farm = Farm(self.interface, self.keypair)
        self.contract = Contract(self.interface, self.keypair)
        self.entity = Entity(self.interface, self.keypair)

    @property
    def interface(self):
        if not self._interface:
            self._interface = SubstrateInterface(
                url=self.url, ss58_format=42, type_registry=self.type_registry, type_registry_preset="polkadot"
            )
        return self._interface

    @property
    def keypair(self):
        if not self._keypair:
            self._keypair = Keypair.create_from_mnemonic(self.words, crypto_type=self.crypto_type.value)  # FIXME
        return self._keypair

    @property
    def address(self):
        return self.keypair.ss58_address

    def load_default_type_registry(self):
        """Load default type registry json to object type_registry"""
        self.type_registry = j.data.serializers.json.load_from_file(TYPES_PATH)
        return self.type_registry

    # def sign_twin_entity(self, entity_id):
    #     # TODO
    #     import hashlib

    #     twin_id = self.twin.get_id()
    #     if not twin_id:
    #         raise ValueError("No twin with twin id found")

    #     entity = self.entity.get(entity_id=entity_id)
    #     if not entity_id:
    #         raise ValueError("No entity with entity id found")

    #     message = "0x" + self.challenge_hash()

    #     out = bytearray()
    #     out += entity_id.to_bytes(4, "big")
    #     out += twin_id.to_bytes(4, "big")
    #     message = hashlib.md5(out.encode()).hexdigest()
    #     signed_msg = self.keypair.sign(message)[2:]
    #     # return self.keypair.sign(out.decode())[2:]

    def generatMnemonic(self):
        return Keypair.generate_mnemonic()


# async def signEntityCreation(self, name, country_id, city_id):
#   out = bytearray()
#   out += name.encode()
#   out += country_id.to_bytes(4, "big")
#   out += city_id.to_bytes(4, "big")
#   return self.keypair.sign(out.decode())[2:]
#   # return signEntityCreation(this, name, countryID, cityID)


#   async updateEntity (name, countryID, cityID, callback) {
#     return updateEntity(this, name, countryID, cityID, callback)
#   }

#   async createEntity (target, name, countryID, cityID, signature, callback) {
#     return createEntity(this, target, name, countryID, cityID, signature, callback)
#   }

#   async listEntities () {
#     return listEntities(this)
#   }

#   async deleteEntity (callback) {
#     return deleteEntity(this, callback)
#   }

#   async addTwinEntity (twinID, entityID, signature, callback) {
#     return addTwinEntity(this, twinID, entityID, signature, callback)
#   }

#   async deleteTwinEntity (twinID, entityID, callback) {
#     return deleteTwinEntity(this, twinID, entityID, callback)
#   }


#   async getPrice () {
#     return getPrice(this)
#   }

#   async vest (locked, perBlock, startingBlock, tftPrice, callback) {
#     return vestedTransfer(this, locked, perBlock, startingBlock, tftPrice, callback)
#   }

#   async getBalance () {
#     return getBalance(this, this.address)
#   }

#   async getBalanceOf (address) {
#     return getBalance(this, address)
#   }

#   async transfer (address, amount, callback) {
#     return transfer(this, address, amount, callback)
#   }

#   async proposeTransaction (transactionID, to, amount, callback) {
#     return proposeTransaction(this, transactionID, to, amount, callback)
#   }

#   async voteTransaction (transactionID, callback) {
#     return voteTransaction(this, transactionID, callback)
#   }


#   async verify (message, signature, pubkey) {
#     return this.key.verify(message, signature, pubkey)
#   }
