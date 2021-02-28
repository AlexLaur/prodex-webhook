# -*- coding: utf-8 -*-
#
# - decorators -
#
# All decorators usefull for the Webhook.
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

from functools import wraps

from flask import request, abort

from . import utils


def check_signature(secret_key: str):
    """Check the signature of the incoming request.
    If the calculated signature correspond to the incoming signature, the
    fucntion will be executed. If not, 403 (Forbidden) is return.

    :param secret_key: The secret key which is used by the sender to generate
    the signature.
    :type secret_key: str
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not utils.proxy_signature_is_valid(
                request=request, secret=secret_key
            ):
                abort(403)
            return func(*args, **kwargs)

        return wrapper

    return decorator
