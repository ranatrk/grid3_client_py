import pdb
from jumpscale.loader import j
from jumpscale.clients.base import Client
from jumpscale.core.base import fields


class RmbHttp(Client):
    proxy_url = fields.String()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _check_valid_destination(self, destination: list):
        if len(destination) > 1:
            raise ValueError("Http client does not support multi destinations")
        elif not destination:
            raise ValueError("The message destination is empty")

    def prepare(self, command: str, destination: list, expiration: int, retry: int) -> dict:
        if not destination:
            raise ValueError("destination needs to be provided")
        msg = {
            "ver": 1,
            "uid": "",
            "cmd": command,
            "exp": expiration,
            "dat": "",
            "src": destination[0] or 0,
            "dst": destination,
            "ret": "",
            "try": retry,
            "shm": "",
            "now": j.data.time.now().timestamp,
            "err": "",
        }
        return msg

    def send(self, message: dict, payload: str):
        message["dat"] = str(j.data.serializers.base64.encode(payload))
        destination = message.get("dst", [])
        retries = message.get("try", 1)

        self._check_valid_destination(destination)

        request_body = j.data.serializers.json.dumps(message)
        url = f"{self.proxy_url}/twin/{destination[0]}"

        for i in range(retries):
            try:
                j.logger.info(f"Sending trial {i+1}: {url}")
                res = j.tools.http.post(url, request_body)
                if res.status_code < 200 or res.status_code > 300:
                    raise j.tools.http.HTTPError(f"Request failed {res.reason}")
                j.logger.info(f"Sending trial {i+1}: Success")
                msgIdentifier = res.json()

                j.logger.info(msgIdentifier)
                message["ret"] = msgIdentifier["retqueue"]
                return message
            except Exception as e:
                if i < retries:
                    j.logger.warning(f"trial {i}: cannot send the message, Message: {str(e)}")
                else:
                    raise e

    def read(self, message: dict) -> dict:
        destination = message.get("dst", [])
        retries = message.get("try", 1)
        retqueue = message.get("ret", "")

        self._check_valid_destination(destination)
        url = f"{self.proxy_url}/twin/{destination[0]}/{retqueue}"

        if not retqueue:
            raise ValueError("The message retqueue is null")

        for i in range(retries):
            try:
                j.logger.info(f"Reading trial {i}: {url}")
                res = j.tools.http.post(url)
                return res.json()
            except Exception as e:
                if i < retries:
                    j.logger.warning(f"trial {i}: cannot read the message, Message: {str(e)}")
                else:
                    raise e
        return {}
