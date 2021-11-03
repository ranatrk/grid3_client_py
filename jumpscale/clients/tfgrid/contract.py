import asyncio
from .interface_client import InterfaceClient

MODULE_NAME = "SmartContractModule"


class Contract(InterfaceClient):

    # create node contract creates a contract
    def create_node_contract(self, nodeID, data, hash, numberOfPublicIPs):
        """Create/deploy a new node contract

        :param nodeID: nodeId to deploy contract
        :type nodeID: int
        :param data: data in contract
        :type data: str
        :param hash: deployment hash
        :type hash: str
        :param numberOfPublicIPs: number of public IPs to include
        :type numberOfPublicIPs: int
        Raises:
            RuntimeError: if submitted extrinsic failed

        Returns: extrinsic result
        """
        params = {"node_id": nodeID, "data": data, "deployment_hash": hash, "public_ips": numberOfPublicIPs}

        submitted_extrinsic = self.submit_signed_extrinsic(
            call_module=MODULE_NAME, call_function="create_node_contract", call_params=params
        )

        if submitted_extrinsic:

            if submitted_extrinsic.finalized and submitted_extrinsic.is_success:
                for event in submitted_extrinsic.triggered_events:
                    event_dict = event.serialize()
                    # check for extrinsic success/failure
                    if (
                        event_dict.get("module_id", "") == MODULE_NAME
                        and event_dict.get("event_id", "") == "ContractCreated"
                    ):

                        attributes = event_dict.get("attributes", [])
                        results = [item["value"] for item in attributes]
                        return results
                return []  ## FIXME
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
        """Get a contract

        :param id: contract id to query [only]
        :type id: int
        OR
        :param hash: data hash contract was created with
        :type hash: str
        :param node_id: node id contract was created with
        :type node_id: int
        Raises:
            RuntimeError: if submitted extrinsic failed to get contract id for querying

        :return contract: dict
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
        Get node contracts with passed id

        :param id: contract id to query [only]
        :type id: int

        :return contract : list of dict
        """
        if not id:
            raise ValueError("No id provided")

        contracts = self.query(module=MODULE_NAME, storage_function="NodeContracts", params=[id])

        return contracts

    def update_node_contract(self, contract_id, data, hash):  # TODO

        params = {"contract_id": contract_id, "data": data, "deployment_hash": hash}

        submitted_extrinsic = self.submit_signed_extrinsic(
            call_module=MODULE_NAME, call_function="update_node_contract", call_params=params
        )

        # check submitted_extrinsic.is_success
        if submitted_extrinsic:
            if submitted_extrinsic.is_success and submitted_extrinsic.finalized:
                return True
            else:
                raise RuntimeError(submitted_extrinsic.error_message)

    def cancel(self, id):
        """Cancel deployed contract by id
        :param id: contract id
        :type id: int

        :return: submitted extrinsic result
        """
        submitted_extrinsic = self.submit_signed_extrinsic(
            call_module=MODULE_NAME, call_function="cancel_contract", call_params={"contract_id": id}
        )
        if submitted_extrinsic:
            if submitted_extrinsic.is_success and submitted_extrinsic.finalized:
                return True
            else:
                raise RuntimeError(submitted_extrinsic.error_message)
