from .interface_client import InterfaceClient

MODULE_NAME = "TfgridModule"


class Farm(InterfaceClient):
    def create(self, name, ips):
        if not ips:
            raise ValueError("Ips should be provided")
        if not name:
            raise ValueError("Farm name should be provided")

        submitted_extrinsic = self.submit_signed_extrinsic(
            call_module=MODULE_NAME, call_function="create_farm", call_params={"name": name, "public_ips": ips}
        )
        if submitted_extrinsic and submitted_extrinsic.is_success:
            return submitted_extrinsic
        else:
            raise RuntimeError(submitted_extrinsic.error_message)

    def get(self, id: int = None, name: str = None):
        if name:
            if not id:
                id = self.query(module=MODULE_NAME, storage_function="FarmIdByName", params=[name])

            else:
                raise ValueError("Only query item should be passed. Either Farm id or Farm name")
        elif not id:
            raise ValueError("You must pass a valid farm id or name")

        farm_obj = self.query(module=MODULE_NAME, storage_function="Farms", params=[id])  # TODO add await for async

        if farm_obj["id"] != id:
            raise KeyError("No such farm found")

        return farm_obj

    def update(self, id, name, pricing_policy_id):

        params = {"id": id, "name": name, "pricing_policy_id": pricing_policy_id}

        submitted_extrinsic = self.submit_signed_extrinsic(
            call_module=MODULE_NAME, call_function="update_farm", call_params=params
        )

        if submitted_extrinsic:
            if submitted_extrinsic.is_success and submitted_extrinsic.finalized:
                return True
            else:
                raise RuntimeError(submitted_extrinsic.error_message)

    def delete(self, id):
        submitted_extrinsic = self.submit_signed_extrinsic(
            call_module=MODULE_NAME, call_function="delete_farm", call_params={"id": id}
        )
        if submitted_extrinsic and submitted_extrinsic.is_success:
            return True
        else:
            raise RuntimeError(submitted_extrinsic.error_message)

    # List all farms
    def list(self):
        return self.query_map(module=MODULE_NAME, storage_function="Farms")
