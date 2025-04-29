import base64
import hmac
import json
import logging
import os
import time
import urllib.parse
from collections import OrderedDict
from hashlib import sha256
from typing import Any, Dict, Optional

# 检查必要的依赖是否已安装
try:
    import requests
    from requests import get as requests_get
except ImportError:
    raise ImportError(
        "使用openapi_util模块需要安装requests库。"
        "请使用 'pip install pxtool[openapi]' 安装额外依赖。"
    )

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
LOCAL_CACHE: Dict[str, Any] = {}
DEFAULT_CACHE_TIME = 1800  # seconds


class GatewayException(Exception):
    """Custom Exception for DCC errors."""
    pass


class ApiGatewayService:
    def __init__(self, ucg_config: Dict[str, str]):
        self.ucg_config = ucg_config

    def get_token(self, force_refresh: bool = False) -> str:
        """
        Get access token using local in-memory cache.
        :param force_refresh: Force fetch a new token
        :return: Access token string
        """
        cache_key = 'GATEWAY_ACCESS_TOKEN'
        now = time.time()

        # Step 1: Try local cache
        token_info = LOCAL_CACHE.get(cache_key)
        if token_info and not force_refresh:
            token, expire_at = token_info
            if expire_at > now:
                logger.info("Using token from LOCAL cache.")
                return token

        # Step 2: Fetch new token from remote
        params = self.build_params_map(self.ucg_config['app_key'], str(int(now * 1000)))
        signature = self.sign(params, self.ucg_config['app_secret'])
        logger.info(f"Requesting token with signature: {signature}")

        url = self.build_token_url(params['appKey'], params['timestamp'], signature)
        response = requests_get(url).text
        logger.info(f"Token response: {response}")

        if not response:
            raise GatewayException("Failed to get token: Empty response.")

        result = json.loads(response)
        if not result or not result.get("data"):
            raise GatewayException("Failed to get token: Invalid result.")

        token = result["data"]["access_token"]
        expire_seconds = result["data"].get("expire", DEFAULT_CACHE_TIME)

        # Save to local cache
        LOCAL_CACHE[cache_key] = (token, now + expire_seconds - 60)  # Reserve 1 minute before expiry

        return token

    @staticmethod
    def build_params_map(app_key: str, timestamp: str) -> OrderedDict:
        return OrderedDict([
            ('appKey', app_key),
            ('timestamp', timestamp)
        ])

    @staticmethod
    def sign(params: OrderedDict, secret_key: str) -> str:
        try:
            sorted_params = OrderedDict(sorted(params.items()))
            string_to_sign = ''.join(f"{k}{v}" for k, v in sorted_params.items())
            mac = hmac.new(secret_key.encode(), string_to_sign.encode(), sha256)
            signature = base64.b64encode(mac.digest()).decode()
            encoded_signature = urllib.parse.quote(signature).replace('/', '%2F')
            return encoded_signature
        except Exception as e:
            logger.error(f"Failed to sign params: {e}")
            raise GatewayException("Signing failed.")

    def build_token_url(self, app_key: str, timestamp: str, signature: str) -> str:
        path = os.getenv('GATEWAY_TOKEN_URL', '/ucg/oauth/getToken')
        return f"{self.ucg_config['host']}{path}?appKey={app_key}&timestamp={timestamp}&signature={signature}"

    def build_api_request_url(self, api_path: str, token: str, query_params: Optional[Dict[str, Any]] = None) -> str:
        query = {'access_token': token}
        if query_params:
            query.update(query_params)
        query_string = urllib.parse.urlencode(query)
        return f"{self.ucg_config['host']}{api_path}?{query_string}"

    def call_api(self, api_path: str, method: str = 'GET', query_params: Optional[Dict[str, Any]] = None,
                 body: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Any:
        """
        General API call function
        :param api_path: API endpoint suffix
        :param method: HTTP method
        :param query_params: URL query parameters
        :param body: POST body if needed
        :param headers: Optional headers
        :return: Parsed JSON response
        """
        token = self.get_token()

        url = self.build_api_request_url(api_path, token, query_params)
        default_headers = {
            "Content-Type": "application/json",
            "sw8": "llm"
        }
        if headers:
            default_headers.update(headers)

        logger.info(f"Request URL: {url}")
        logger.info(f"Request Method: {method}")

        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=default_headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=default_headers, json=body)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            logger.error(f"HTTP request failed: {e}")
            raise GatewayException(f"API call failed: {e}")