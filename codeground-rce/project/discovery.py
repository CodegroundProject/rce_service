from pyms.flask.services.service_discovery import ServiceDiscoveryBase
import requests
import json


host = "localhost"
port = 8500


class ServiceDiscoveryConsulBasic(ServiceDiscoveryBase):
    def register_service(self, healtcheck_url, app_name, interval=30):
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = {
            "id": "rce",
            "name": app_name,
            "port": 5000,
            "address": "localhost",
            "check": {"name": "ping check", "http": healtcheck_url, "interval": "30s", "status": "passing"},
        }
        response = requests.put(
            "http://{host}:{port}/v1/agent/service/register".format(
                host=host, port=port),
            data=json.dumps(data),
            headers=headers,
        )
        if response.status_code != 200:
            raise Exception(response.content)
