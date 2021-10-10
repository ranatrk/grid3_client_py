import asyncio
from .interface_client import InterfaceClient

MODULE_NAME = "SmartContractModule"


class Contract(InterfaceClient):

    # create node contract creates a contract
    def create_node_contract(self, nodeID, data, hash, numberOfPublicIPs):
        params = {"node_id": nodeID, "data": data, "deployment_hash": hash, "public_ips": numberOfPublicIPs}

        submitted_extrinsic = self.submit_signed_extrinsic(
            call_module=MODULE_NAME, call_function="create_node_contract", call_params=params
        )

        if submitted_extrinsic:
            if submitted_extrinsic.is_success and submitted_extrinsic.finalized:
                return True
            else:
                raise RuntimeError(submitted_extrinsic.error_message)

    def create_name_contract(self, name):
        params = {"name": name}

        submitted_extrinsic = self.submit_signed_extrinsic(
            call_module=MODULE_NAME, call_function="create_name_contract", call_params=params
        )

        if submitted_extrinsic:
            if submitted_extrinsic.is_success and submitted_extrinsic.finalized:
                return True
            else:
                raise RuntimeError(submitted_extrinsic.error_message)

    # getContract gets an contract by id or (hash and node id)
    def get(self, id: int = None, data_hash: str = None, node_id: int = None):
        """
            id (int): contract id only
            OR
            hash (str): data hash contract was created with
            node_id (int): node id contract was created with

        Returns:
            contract : dict
        """
        if not id:
            if not data_hash or not node_id:
                raise ValueError(
                    "You must pass a valid Contract ID or the data_hash and node_id combination the contract was created with"
                )
            else:
                id = self.query(
                    module=MODULE_NAME, storage_function="ContractIDByNodeIDAndHash", params=[node_id, data_hash]
                )
                if not id:
                    raise ValueError("No contract found corresponding to data_hash and node_id provided")

        contract = self.query(module=MODULE_NAME, storage_function="Contracts", params=[id])

        return contract

    def get_node_contract(self, id: int = None):  # TODO test
        """
            id (int): contract id only


        Returns:
            contract : list of dict
        """
        if not id:
            raise ValueError("No id provided")

        contracts = self.query(module=MODULE_NAME, storage_function="NodeContracts", params=[id])

        return contracts

    def update(self, contract_id, data, hash):  # TODO

        params = {"contract_id": contract_id, "data": data, "deployment_hash": hash}

        submitted_extrinsic = self.submit_signed_extrinsic(
            call_module=MODULE_NAME, call_function="update_contract", call_params=params
        )

        # check submitted_extrinsic.is_success
        if submitted_extrinsic:
            if submitted_extrinsic.is_success and submitted_extrinsic.finalized:
                return True
            else:
                raise RuntimeError(submitted_extrinsic.error_message)

    def cancel(self, id):
        submitted_extrinsic = self.submit_signed_extrinsic(
            call_module=MODULE_NAME, call_function="cancel_contract", call_params={"contract_id": id}
        )
        if submitted_extrinsic:
            if submitted_extrinsic.is_success and submitted_extrinsic.finalized:
                return True
            else:
                raise RuntimeError(submitted_extrinsic.error_message)
