# RMB HTTP Client

A http client an the rmb proxy deployed. The client sends/recieves through http requests to/from the rmb proxy which handles them using redis.

## Client configurations

To setup the client, it should be provided with the proxy's `url` and the user's `twin id`:

```python
rmb_proxy_client = j.clients.rmb_http.get("test", proxy_url=RMB_PROXY_URL, twin_id=USER_TWIN_ID)
```

where `proxy_url` depends on the network being used:

- Devnet: https://gridproxy.dev.grid.tf
- Testnet: https://gridproxy.test.grid.tf

## Client usage

To send and recieve a response the following steps should be followed:

**note** examples associated for getting a deployment using the contract id

1. Prepare the message to be send using the `pepare` function

    ```python
    REDIS_COMMAND = "zos.deployment.get"
    DEST_NODE_TWIN_ID = 2
    prepare = rmb_proxy_client.prepare(command=REDIS_COMMAND, destination=[DEST_NODE_TWIN_ID], expiration=20, retry=2)
    ```

2. Prepare the payload to be sent

    ```python
    CONTRACT_ID = 130
    payload = j.data.serializers.json.dumps({"contract_id": CONTRACT_ID})
    ```

3. Send the payload and prepared message to the rmb proxy using the `send` function

    ```python
    request = rmb_proxy_client.send(prepare, payload=payload)
    ```

4. Read the result using the rmb proxy associated with the sent data using the `read` function

    ```python
    deployment_result = rmb_proxy_client.read(request)
    ```
