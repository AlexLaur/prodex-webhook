# -*- coding: utf-8 -*-
#
# - utils -
#
# Collection of functions for the Prodex Webhook
#
# Copyright (c) 2020 Prodex
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import hmac
import base64
import hashlib

import yaml


def load_config_file(path: str) -> dict:
    """Load the configuration from the config file

    :param path: THe config file to load
    :type path: str
    :return: The configuration
    :rtype: dict
    """
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config


def get_proxy_signature(query_dict: dict, secret: str) -> str:
    """Calculate the signature of the given query dict and the secret key.

    :param query_dict: The data from the endpoint
    :type query_dict: dict
    :param secret: The secret key
    :type secret: str
    :return: The calculated signature
    :rtype: str
    """
    # Sort and combine query parameters into a single string.
    sorted_params = ""
    for key in sorted(query_dict.keys()):
        sorted_params += "{0}={1}".format(key, query_dict.get(key))

    _secret = bytes(secret, encoding="utf8")

    signature = hmac.new(
        _secret, sorted_params.encode("utf-8"), hashlib.sha256
    )
    return signature.hexdigest()


def proxy_signature_is_valid(request: object, secret: str) -> bool:
    """Return true if the calculated signature matches that present
    in the query string of the given request.

    :param request: The request from the webhook
    :type request: object
    :param secret: The secret key
    :type secret: str
    :return: The result of the calculation
    :rtype: bool
    """
    signature_to_verify = request.headers.get("X-Prodex-Signature", None)
    if not signature_to_verify:
        return False

    query_dict = request.get_json()

    calculated_signature = get_proxy_signature(query_dict, secret)

    # Try to use compare_digest() to reduce vulnerability to timing attacks.
    # If it's not available, just fall back to regular string comparison.
    try:
        return hmac.compare_digest(calculated_signature, signature_to_verify)
    except AttributeError:
        return calculated_signature == signature_to_verify
