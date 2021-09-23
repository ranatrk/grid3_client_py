from substrateinterface import Keypair
from substrateinterface import exceptions as substrateinterface_exceptions, SubstrateInterface


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
            raise e  # TODO handle exception

        return result.value

    def query_map(self, module, storage_function) -> list:
        try:
            result_list = self.interface.query_map(module=module, storage_function=storage_function)
            result = [record[1].value for record in result_list.records]
        except substrateinterface_exceptions.StorageFunctionNotFound as e:
            raise e  # TODO handle exception

        return result

    def compose_call(self, call_module, call_function, call_params):
        try:
            call = self.interface.compose_call(
                call_module=call_module, call_function=call_function, call_params=call_params
            )
        except substrateinterface_exceptions.StorageFunctionNotFound as e:
            raise e  # TODO handle exception

        return call

    def create_signed_extrinsic(self, call, keypair=None, era=None, nonce=None, tip=0, signature=None):
        if not keypair:
            keypair = self.keypair

        return self.interface.create_signed_extrinsic(
            call=call, keypair=keypair, era=era, nonce=nonce, tip=tip, signature=signature
        )

    def submit_extrinsic(self, signed_extrinsic, wait_for_inclusion=False, wait_for_finalization=False):

        submited_extrinsic = self.interface.submit_extrinsic(
            extrinsic=signed_extrinsic,
            wait_for_inclusion=wait_for_inclusion,
            wait_for_finalization=wait_for_finalization,
        )
        return submited_extrinsic

    def submit_signed_extrinsic(
        self, call_module, call_function, call_params=None, wait_for_inclusion=True, wait_for_finalization=True
    ):
        call_params = call_params or {}
        call = self.compose_call(call_module=call_module, call_function=call_function, call_params=call_params)
        signed_extrinsic = self.create_signed_extrinsic(call=call)

        submited_extrinsic = self.submit_extrinsic(
            signed_extrinsic, wait_for_inclusion=wait_for_inclusion, wait_for_finalization=wait_for_finalization
        )
        return submited_extrinsic

