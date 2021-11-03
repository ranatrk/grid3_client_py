# TFGrid client (Development)

A jumpscale client that enables interaction with substrate

## Client configuration

To create a client, a substrate url needs to be provided and the words/mnemonics generated from account creation.

- **url**: substrate url

    Deployed:
    - Devnet: `"wss://tfchain.dev.threefold.io/ws"` [DEFAULT]
    - Testnet: `"wss://tfchain.test.threefold.io/ws"`
- **words**: mnemonics generated from account creation
- **type_registry** (optional): dict with the type registry to be used, if not provided the type registry is loaded from [types.json](types.json)

Example:

```python
url = "wss://tfchain.dev.threefold.io/ws"
words = "ring today nice tiger obtain neglect little bread client night another welcome"
tfgrid_client = j.clients.tfgrid.get("test", url, words)
tfgrid_client.save()
```

## Client updating

### Updating default type registry and loading it

The loaded default [types registry](types.json) can be updated manually according to remote registry then reloaded from the jsng shell.

```python
tfgrid_client = j.clients.tfgrid.test
tfgrid_client.load_default_type_registry()
tfgrid_client.save()
```

### Adding new module usage

- import **InterfaceClient**
- for extrinsics:

    `submit_signed_extrinsic(call_module, call_function, call_params, wait_for_inclusion, wait_for_finalization)`

- for queries:

    `query(module, storage_function, params)`

- for query maps:

    `query_map(module, storage_function)`

- Example

    ```python
    from .interface_client import InterfaceClient

    MODULE_NAME = "TfgridModule"

    class Farm(InterfaceClient):
        # Create signed extrinsic
        def create(self, name, ips):
            submitted_extrinsic = self.submit_signed_extrinsic(
                call_module=MODULE_NAME, call_function="create_farm", call_params={"name": name, "public_ips": ips}
            )
            if submitted_extrinsic and submitted_extrinsic.is_success:
                return submitted_extrinsic
            else:
                raise RuntimeError(submitted_extrinsic.error_message)

        # Query
        def get(self, id):
            farm_obj = self.query(module=MODULE_NAME, storage_function="Farms", params=[id])

            if farm_obj["id"] != id:
                raise KeyError("No such farm found")

            return farm_obj

        # Query map
        def list(self):
            return self.query_map(module=MODULE_NAME, storage_function="Farms")
    ```
