import asyncio

from jumpscale.sals.zos.deployment import Deployment, SignatureRequirement, SignatureRequest
from jumpscale.loader import j

RMB_PROXY_URL = "https://gridproxy.dev.grid.tf"


def test():
    twin_id = 166
    url = "wss://tfchain.dev.grid.tf/ws"
    node_id = 17
    node_twin_id = 19

    rmb_proxy_client = j.clients.rmb_http.get("test1", proxy_url=RMB_PROXY_URL, twin_id=twin_id)
    contract_id = 4240

    prepare = rmb_proxy_client.prepare(command="zos.deployment.get", destination=[node_twin_id], expiration=20, retry=2)
    payload = j.data.serializers.json.dumps({"contract_id": contract_id})
    deployment_request = rmb_proxy_client.send(prepare, payload=payload)
    deployment_result = rmb_proxy_client.read(deployment_request)
    deployment = j.data.serializers.json.loads(deployment_result[0]["dat"])

    print(deployment)


print(test())
