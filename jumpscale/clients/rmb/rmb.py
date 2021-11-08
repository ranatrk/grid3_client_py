import uuid
from jumpscale.clients.base import Client
from jumpscale.clients.redis.redis import RedisClient
from jumpscale.core.base import fields
from jumpscale.loader import j


class Rmb(RedisClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def prepare(self, command: str, dst: list, exp: int, num_retry: int):
        msg = {
            "version": 1,
            "id": "",
            "command": command,
            "expiration": exp,
            "retry": num_retry,
            "data": "",
            "twin_src": 0,
            "twin_dst": dst,
            "retqueue": uuid.uuid4(),
            "schema": "",
            "epoch": j.data.time.now().timestamp,
            "err": "",
        }
        return msg

    def send(self, message, payload):
        message["data"] = str(j.data.serializers.base64.encode(payload))

        request = j.data.serializers.json.dumps(message)
        print(request)
        self.lpush("msgbus.system.local", request)

    def read(self, message):
        print("Waiting reply $msg.retqueue")
        responses = []
        while len(responses) < len(message.get("twin_dst", [])):
            results = self.blpop(message["retqueue"])
            response = j.data.serializers.json.loads(results[1])

            response_message = j.data.serializers.base64.decode(response)
            responses.append(response_message)

        return responses
