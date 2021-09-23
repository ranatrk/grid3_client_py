# const { ApiPromise, WsProvider, Keyring } = require('@polkadot/api')
# const crypto = require('@polkadot/util-crypto')
# const types = require('../types.json')
# const bip39 = require('bip39')

# const { getEntity, deleteEntity, createEntity, updateEntity, listEntities, getEntityIDByName, getEntityIDByPubkey } = require('./entity')
# const { createTwin, getTwin, deleteTwin, addTwinEntity, deleteTwinEntity, listTwins } = require('./twin')
# const { createFarm, getFarm, deleteFarm, listFarms, addFarmIP, deleteFarmIP } = require('./farms')
# const { createNode, updateNode, getNode, getNodeIDByPubkey, deleteNode, listNodes } = require('./node')
# const { signEntityTwinID, signEntityCreation } = require('./sign')
# const { getPrice } = require('./price')
# const { vestedTransfer } = require('./vesting')
# const { getBalance, transfer } = require('./balance')
# const { proposeTransaction, voteTransaction, listValidators } = require('./voting')
# const { createContract, updateContract, cancelContract, getContract } = require('./contract')
import json
from substrateinterface import Keypair, KeypairType, SubstrateInterface
from .twin import Twin
from .farm import Farm
from .contract import Contract

from jumpscale.clients.base import Client
from jumpscale.core.base import fields
from jumpscale.loader import j

TYPES_PATH = "jumpscale/clients/tfgrid/types.json"

class TfgridClient(Client):
    url = fields.String()
    words = fields.String()
    type_registry = fields.Typed(dict)
    keypair = fields.Typed(Keypair)
    interface = fields.Typed(SubstrateInterface)

    def __init__(self, url="", words="", type_registry=None, **kwargs):
        super().__init__(url=url, words=words, type_registry=type_registry, **kwargs)
        self.url = url
        self.words = words or self.generatMnemonic()
        self.keypair = Keypair.create_from_mnemonic(self.words, crypto_type=KeypairType.ED25519)
        self.type_registry = type_registry or j.data.serializers.json.load_from_file(TYPES_PATH)
        self.interface = SubstrateInterface(url=self.url, ss58_format=42, type_registry=self.type_registry)

        self.twin = Twin(self.interface, self.keypair)
        self.farm = Farm(self.interface, self.keypair)
        self.contract = Contract(self.interface, self.keypair)

    # @property
    def load_type_registry(self):
        # if not self._type_registry:
        # f = open("types.json")
        # self.type_registry = json.load(f)
        self.type_registry = j.data.serializers.json.load_from_file(TYPES_PATH) 
        return self.type_registry

    # @property
    # def interface(self):
    #     if not self._interface:
    #         self._interface = SubstrateInterface(url=self.url, ss58_format=42, type_registry=self.type_registry)
    #     return self._interface

    # @property
    # def keypair(self):
    #     if not self._keypair:
    #         self._keypair = Keypair.create_from_mnemonic(self.words, crypto_type=KeypairType.ED25519)
    #     return self._keypair

    @property
    def address(self):
        return self.keypair.ss58_address

    # @property
    # def twin(self):
    #     if not self._twin:
    #         self._twin = Twin(self.interface, self.keypair)
    #     return self._twin

    # @property
    # def farm(self):
    #     if not self._farm:
    #         self._farm = Farm(self.interface, self.keypair)
    #     return self._farm

    # @property
    # def contract(self):
    #     if not self._contract:
    #         self._contract = Contract(self.interface, self.keypair)
    #     return self._contract

    def generatMnemonic(self):
        return Keypair.generate_mnemonic()


# async init () {
#   const api = await getPolkaAPI(this.url)
#   const keyring = new Keyring({ type: 'ed25519' })

#   if (!this.words) {
#     this.words = crypto.mnemonicGenerate()
#   } else {
#     if (!bip39.validateMnemonic(this.words)) {
#       throw Error('Invalid mnemonic! Must be bip39 compliant')
#     }
#   }

#   const key = keyring.addFromMnemonic(this.words)
#   this.key = key
#   console.log(`Key with address: ${this.key.address} is loaded.`)

#   this.keyring = keyring
#   this.address = this.key.address

#   this.api = api
# }

# async createMnemonic () {
#   return crypto.mnemonicGenerate()
# }

# async def sign(self,entity_id, twin_id):
#   out = bytearray()
#   # out += name.encode()
#   out += entity_id.to_bytes(4, "big")
#   out += twin_id.to_bytes(4, "big")
#   return self.keypair.sign(out.decode())[2:]

#   # return signEntityTwinID(this, entityID, twinID)


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

#   async getEntityByID (id) {
#     return getEntity(this, id)
#   }

#   async getEntityIDByName (name) {
#     return getEntityIDByName(this, name)
#   }

#   async getEntityIDByPubkey (pubkey) {
#     return getEntityIDByPubkey(this, pubkey)
#   }

#   async listEntities () {
#     return listEntities(this)
#   }

#   async deleteEntity (callback) {
#     return deleteEntity(this, callback)
#   }

#   async createTwin (ip, callback) {
#     return createTwin(this, ip, callback)
#   }

#   async getTwinByID (id) {
#     return getTwin(this, id)
#   }

#   async listTwins () {
#     return listTwins(this)
#   }

#   async deleteTwin (id, callback) {
#     return deleteTwin(this, id, callback)
#   }

#   async addTwinEntity (twinID, entityID, signature, callback) {
#     return addTwinEntity(this, twinID, entityID, signature, callback)
#   }

#   async deleteTwinEntity (twinID, entityID, callback) {
#     return deleteTwinEntity(this, twinID, entityID, callback)
#   }

#   async createFarm (name, certificationType, publicIPs, callback) {
#     return createFarm(this, name, certificationType, publicIPs, callback)
#   }

#   async addFarmIp (id, ip, gateway, callback) {
#     return addFarmIP(this, id, ip, gateway, callback)
#   }

#   async deleteFarmIp (id, ip, callback) {
#     return deleteFarmIP(this, id, ip, callback)
#   }

#   async getFarmByID (id) {
#     return getFarm(this, id)
#   }

#   async listFarms () {
#     return listFarms(this)
#   }

#   async deleteFarmByID (id, callback) {
#     return deleteFarm(this, id, callback)
#   }

#   async createNode (farmID, resources, location, countryID, cityID, publicConfig, callback) {
#     return createNode(this, farmID, resources, location, countryID, cityID, publicConfig, callback)
#   }

#   async updateNode (nodeID, farmID, resources, location, countryID, cityID, publicConfig, callback) {
#     return updateNode(this, nodeID, farmID, resources, location, countryID, cityID, publicConfig, callback)
#   }

#   async getNodeByID (id) {
#     return getNode(this, id)
#   }

#   async getNodeByPubkey (id) {
#     return getNodeIDByPubkey(this, id)
#   }

#   async listNodes () {
#     return listNodes(this)
#   }

#   async deleteNode (id, callback) {
#     return deleteNode(this, id, callback)
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

#   async listValidators () {
#     return listValidators(this)
#   }

#   async verify (message, signature, pubkey) {
#     return this.key.verify(message, signature, pubkey)
#   }

#   async createContract (nodeID, data, deploymentHash, publicIPS, callback) {
#     return createContract(this, nodeID, data, deploymentHash, publicIPS, callback)
#   }

#   async updateContract (contractID, data, hash, callback) {
#     return updateContract(this, contractID, data, hash, callback)
#   }

#   async cancelContract (contractID, callback) {
#     return cancelContract(this, contractID, callback)
#   }

#   async getContractByID (id) {
#     return getContract(this, id)
#   }
# }

# async function getPolkaAPI (url) {
#   if (!url || url === '') {
#     url = 'ws://localhost:9944'
#   }

#   const provider = new WsProvider(url)
#   return ApiPromise.create({ provider, types })
# }

# module.exports = { Client }
