from substrateinterface import Keypair
from substrateinterface import exceptions as substrateinterface_exceptions, SubstrateInterface

ERRORS_MAP = {
    # order same as :
    # https://github.com/threefoldtech/tfchain_pallets/blob/f0bb8747d7c70769c77cf814d8f02384b211c88d/pallet-smart-contract/src/lib.rs#L59
    "SmartContractModule": [
        "TwinNotExists",
        "NodeNotExists",
        "FarmNotExists",
        "FarmHasNotEnoughPublicIPs",
        "FarmHasNotEnoughPublicIPsFree",
        "FailedToReserveIP",
        "FailedToFreeIPs",
        "ContractNotExists",
        "TwinNotAuthorizedToUpdateContract",
        "TwinNotAuthorizedToCancelContract",
        "NodeNotAuthorizedToDeployContract",
        "NodeNotAuthorizedToComputeReport",
        "PricingPolicyNotExists",
        "ContractIsNotUnique",
        "NameExists",
        "NameNotValid",
    ],
    # order same as :
    # https://github.com/threefoldtech/tfchain_pallets/blob/f0bb8747d7c70769c77cf814d8f02384b211c88d/pallet-tfgrid/src/lib.rs#L129
    "TfgridModule": [
        "NoneValue",
        "StorageOverflow",
        "CannotCreateNode",
        "NodeNotExists",
        "NodeWithTwinIdExists",
        "CannotDeleteNode",
        "NodeDeleteNotAuthorized",
        "NodeUpdateNotAuthorized",
        "FarmExists",
        "FarmNotExists",
        "CannotCreateFarmWrongTwin",
        "CannotUpdateFarmWrongTwin",
        "CannotDeleteFarm",
        "CannotDeleteFarmWrongTwin",
        "IpExists",
        "IpNotExists",
        "EntityWithNameExists",
        "EntityWithPubkeyExists",
        "EntityNotExists",
        "EntitySignatureDoesNotMatch",
        "EntityWithSignatureAlreadyExists",
        "CannotUpdateEntity",
        "CannotDeleteEntity",
        "SignatureLenghtIsIncorrect",
        "TwinExists",
        "TwinNotExists",
        "TwinWithPubkeyExists",
        "CannotCreateTwin",
        "UnauthorizedToUpdateTwin",
        "PricingPolicyExists",
        "PricingPolicyNotExists",
        "CertificationCodeExists",
        "FarmingPolicyAlreadyExists",
    ],
}


class InterfaceClient:
    interface: SubstrateInterface

    def __init__(self, interface_client: SubstrateInterface, keypair: Keypair):
        self.interface = interface_client
        self.keypair = keypair

    def query(self, module, storage_function, params):
        params = params or []
        try:
            result = self.interface.query(module=module, storage_function=storage_function, params=params)
        except substrateinterface_exceptions.StorageFunctionNotFound as e:
            raise e

        return result.value

    def query_map(self, module, storage_function) -> list:
        try:
            result_list = self.interface.query_map(module=module, storage_function=storage_function)
            result = [record[1].value for record in result_list.records]
        except substrateinterface_exceptions.StorageFunctionNotFound as e:
            raise e

        return result

    def compose_call(self, call_module, call_function, call_params):
        try:
            call = self.interface.compose_call(
                call_module=call_module, call_function=call_function, call_params=call_params
            )
        except substrateinterface_exceptions.StorageFunctionNotFound as e:
            raise e

        return call

    def create_signed_extrinsic(self, call, keypair=None, era=None, nonce=None, tip=0, signature=None):
        if not keypair:
            keypair = self.keypair

        return self.interface.create_signed_extrinsic(
            call=call, keypair=keypair, era=era, nonce=nonce, tip=tip, signature=signature
        )

    def submit_extrinsic(self, signed_extrinsic, wait_for_inclusion=False, wait_for_finalization=False):

        submitted_extrinsic = self.interface.submit_extrinsic(
            extrinsic=signed_extrinsic,
            wait_for_inclusion=wait_for_inclusion,
            wait_for_finalization=wait_for_finalization,
        )

        if submitted_extrinsic.triggered_events:
            for event in submitted_extrinsic.triggered_events:
                event_dict = event.serialize()
                # check for extrinsic success/failure

                if event_dict.get("module_id", "") == "System" and event_dict.get("event_id", "") == "ExtrinsicFailed":
                    err_attributes = event_dict.get("attributes", [])
                    # err = err_attributes[0] if err_attributes else ""
                    err_index = err_attributes[0].get("value", {}).get("Module", {}).get("error", "")
                    module_name = submitted_extrinsic.extrinsic.value["call"]["call_module"]
                    raise RuntimeError(
                        f"Extrinsic Failed for module {module_name} with the following error: {ERRORS_MAP[module_name][err_index]}"
                    )
        return submitted_extrinsic

    def submit_signed_extrinsic(
        self, call_module, call_function, call_params=None, wait_for_inclusion=True, wait_for_finalization=True
    ):
        call_params = call_params or {}
        call = self.compose_call(call_module=call_module, call_function=call_function, call_params=call_params)
        signed_extrinsic = self.create_signed_extrinsic(call=call)

        submitted_extrinsic = self.submit_extrinsic(
            signed_extrinsic, wait_for_inclusion=wait_for_inclusion, wait_for_finalization=wait_for_finalization
        )
        return submitted_extrinsic
