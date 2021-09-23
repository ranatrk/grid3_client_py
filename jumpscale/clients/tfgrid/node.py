from .interface_client import InterfaceClient

MODULE_NAME = "TfgridModule"


class Node(InterfaceClient):
    def get(self, id):
        try:
            id = int(id)
        except Exception as error:
            raise ValueError("ID must be an integer", str(error))

        if not id:
            raise ValueError("You musst pass a valid ID")

        twin_obj = self.query(module=MODULE_NAME, storage_function="Nodes", params=[id])  # TODO add await for async

        if twin_obj["id"] != id:
            raise KeyError("No such twin found")

        return twin_obj

    # List all twins
    def list(self):
        return self.query_map(module=MODULE_NAME, storage_function="Nodes")

