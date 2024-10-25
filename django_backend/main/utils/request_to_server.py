import requests
import dns.resolver
from django.conf import settings


def __ddns_to_ip(domain: str) -> str:
    answers = dns.resolver.resolve(domain, 'A')
    return next(iter(answers)).address


def _request(api_name: str, json: dict, verbose:bool=False):
    host = settings.AI_API_SERVER['HOST']
    port = settings.AI_API_SERVER['PORT']

    base_url = "http://{}:{}/{}"

    try:
        if settings.AI_API_SERVER['IS_DDNS']:
            host = __ddns_to_ip(host)
        url = base_url.format(host, port, api_name)

        if verbose : print(f"Sending request to: '{url}'!")
        response = requests.post(url, json= json, timeout=5)
    except:
        class Response:
            def __init__(self) -> None:
                self.response = {
                    'message' : 'Server not Found!',
                    'code': '404',
                    'url': url,
                }
            def json(self) -> dict[str, str]:
                return self.response
            
        response = Response()
    return response