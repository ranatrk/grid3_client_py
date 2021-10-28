from .interface_client import InterfaceClient

MODULE_NAME = "TfgridModule"


class Twin(InterfaceClient):

    # create creates an entity with given name
    def create(self, ip):
        if not ip:
            raise ValueError("Ip should be provided")

        # call = self.compose_call(call_module=MODULE_NAME, call_function="create_twin", call_params={"ip": ip})
        # signed_extrinsic = self.create_signed_extrinsic(call=call)

        # submit = self.submit_extrinsic(signed_extrinsic, wait_for_inclusion=True)
        submitted_extrinsic = self.submit_signed_extrinsic(
            call_module=MODULE_NAME, call_function="create_twin", call_params={"ip": ip}
        )
        if submitted_extrinsic and submitted_extrinsic.is_success:
            return submitted_extrinsic
        # TODO check submit

    # get gets a twin by id
    def get(self, id):
        try:  # TODO validations
            id = int(id)
        except Exception as error:
            raise ValueError("ID must be an integer", str(error))

        if not id:
            raise ValueError("You must pass a valid ID")

        twin_obj = self.query(module=MODULE_NAME, storage_function="Twins", params=[id])  # TODO add await for async

        if twin_obj["id"] != id:
            raise KeyError("No such twin found")

        return twin_obj

    def get_id(self, public_key: str):
        if not public_key:
            raise ValueError("You must pass a valip public_key")

        twin_id = self.query(module=MODULE_NAME, storage_function="TwinIdByAccountID", params=[public_key])

        if not twin_id:
            raise KeyError("No such twin found")

        return twin_id

    # List all twins
    def list(self):
        return self.query_map(module=MODULE_NAME, storage_function="Twins")

    # deleteTwin deletes the twin linked to this signing key
    def delete(self, id):
        twin = self.get(id)
        submitted_extrinsic = self.submit_signed_extrinsic(
            call_module=MODULE_NAME, call_function="delete_twin", call_params={"twin_id": id}
        )
        if submitted_extrinsic and submitted_extrinsic.is_success:
            return submitted_extrinsic
        else:
            raise RuntimeError(submitted_extrinsic.error_message)

    # addTwinEntity adds an entity to a twin object
    # the signature is a signature provided by the entity that is added.
    # the signature is composed of twinID-entityID as bytes signed by the entity's private key
    # to proof that he in fact approved to be part of this twin
    def add_twin_entity(self, twin_id, entity_id, signature):  # TODO TEST/VERIFY

        submitted_extrinsic = self.submit_signed_extrinsic(
            call_module=MODULE_NAME,
            call_function="add_twin_entity",
            call_params={"twin_id": twin_id, "entity_id": entity_id, "signature": signature},
        )
        if submitted_extrinsic and submitted_extrinsic.is_success:
            return submitted_extrinsic
        else:
            raise RuntimeError(submitted_extrinsic.error_message)

    # deleteTwinEntity delets an entity from a twin
    def delete_twin_entity(self, twin_id, entity_id):  # TODO TEST/VERIFY
        submitted_extrinsic = self.submit_signed_extrinsic(
            call_module=MODULE_NAME,
            call_function="delete_twin_entity",
            call_params={"twin_id": twin_id, "entity_id": entity_id},
        )
        if submitted_extrinsic and submitted_extrinsic.is_success:
            return submitted_extrinsic
        else:
            raise RuntimeError(submitted_extrinsic.error_message)
