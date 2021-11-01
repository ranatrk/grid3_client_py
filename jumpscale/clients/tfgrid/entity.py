from .interface_client import InterfaceClient

MODULE_NAME = "TfgridModule"

# TODO to be tested/verfied
class Entity(InterfaceClient):
    def _sign(self, name, country_id, city_id):
        out = bytearray()
        out += name.encode()
        out += country_id.to_bytes(4, "big")
        out += city_id.to_bytes(4, "big")

        return self.keypair.sign(out.decode())[2:]

    def create(self, name, country_id, city_id, target=None):  # TODO not working FIXME
        if not target:
            target = self.keypair.public_key

        signature = self._sign(name, country_id, city_id)

        params = {
            "target": target,
            "name": name,
            "country": country_id,
            "city": city_id,
            "signature": signature,
        }

        submitted_extrinsic = self.submit_signed_extrinsic(
            call_module=MODULE_NAME, call_function="create_entity", call_params=params
        )
        if submitted_extrinsic and submitted_extrinsic.is_success:
            return submitted_extrinsic
        else:
            raise RuntimeError(submitted_extrinsic.error_message)

    def get(self, entity_id: int = None, account_id: int = None, name: str = None):  # TODO not working FIXME
        if name:
            if not entity_id and not account_id:
                entity_id = self.query(module=MODULE_NAME, storage_function="EntityIdByName", params=[name])
            else:
                raise ValueError("Only one query item should be passed. Either entity_id or name or account_id")
        elif account_id:
            if not entity_id:
                entity_id = self.query(module=MODULE_NAME, storage_function="EntityIdByAccountID", params=[account_id])
            else:
                raise ValueError("Only one query item should be passed. Either entity_id or name or account_id")

        elif not entity_id:
            raise ValueError("You must pass a valid entity_id, or account_id or name")

        entity_obj = self.query(module=MODULE_NAME, storage_function="Entities", params=[entity_id])

        if not entity_obj:
            raise KeyError("No such entity found")

        return entity_obj

    def update(self, name, country_id, city_id):
        params = {"name": name, "country": country_id, "city": city_id}

        submitted_extrinsic = self.submit_signed_extrinsic(
            call_module=MODULE_NAME, call_function="update_entity", call_params=params
        )

        if submitted_extrinsic:
            if submitted_extrinsic.is_success and submitted_extrinsic.finalized:
                return True
            else:
                raise RuntimeError(submitted_extrinsic.error_message)
