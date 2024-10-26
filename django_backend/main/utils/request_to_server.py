import requests
import dns.resolver
from django.conf import settings
import re
import logging
from typing import Optional, Union

logging.basicConfig(
    level=logging.INFO, format='%(levelname)-9s "%(name)s": %(message)s'
)


def __check_ip_or_dns(input_string):
    ip_pattern = re.compile(
        r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    )
    domain_pattern = re.compile(
        r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)(\.[A-Za-z]{2,})+$"
    )

    if ip_pattern.match(input_string):
        return "IP"
    elif domain_pattern.match(input_string):
        return "DNS"
    else:
        return None


def __dns_to_ip(domain: str) -> str:
    answers = dns.resolver.resolve(domain, "A")
    return next(iter(answers)).address


def _request(
    api_name: str,
    json: dict,
    host: Optional[str] = None,
    port: Optional[str] = None,
    protocol: Optional[str] = "http",
    verbose: bool = False,
):
    if host is None:
        host = settings.AI_API_SERVER["HOST"]
        port = settings.AI_API_SERVER["PORT"]
    logger = logging.getLogger(__name__)

    base_url = "{}://{}:{}/{}"

    try:
        checked_host = __check_ip_or_dns(host)

        if checked_host == "DNS":
            host = __dns_to_ip(host)

        protocol = protocol.lower()
        url = base_url.format(protocol, host, port, api_name)

        assert checked_host is not None, "Invalid Domain or IP!"

        if verbose:
            logger.info(f"Sending request to: '{url}'!")

        response = requests.post(url, json=json, timeout=5)
        response.raise_for_status()

    except AssertionError as e:
        message = e
        code = "500"
    except requests.exceptions.Timeout:
        message = "Request Timeout!"
        code = "408"
    except requests.exceptions.ConnectionError:
        message = "Connection error!"
        code = "404"
    except requests.exceptions.HTTPError as err:
        message = f"HTTP error occurred: {err}!"
        code = "404"
    except requests.exceptions.RequestException as err:
        message = f"An error occurred: {err}!"
        code = "404"
    else:
        return response
    finally:
        if verbose:
            logger.error(message)

        class Response:
            def __init__(self) -> None:
                self.response = {
                    "message": message,
                    "code": code,
                    "url": url,
                }

            def json(self) -> dict[str, str]:
                return self.response

        response = Response()
        return response


if __name__ == "__main__":
    valid_ip = "192.168.1.1"
    valid_dns = "truong51972.ddns.net"
    invalid = "1hasfo"

    api_name = "haah"
    data = {"test": "haha"}

    _request(api_name, data, valid_dns, "8000", True)
