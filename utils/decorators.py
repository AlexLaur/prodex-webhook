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

from flask import Response, request, abort

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


def on_event(event_type: str, field_name: list = None):
    """Execute the hook on the specified event.

    Example : An `edit` on a `project` and more specially on the `description` field.
    >>> @on_event(event_type="Change_Project", field_name=["description"])
    >>> function_to_execute():
    >>>     ...

    :param event_type: The type of the event. e.g: `Change_Project`, `New_Contact`
    :type event_type: str
    :param field_name: Field names of the event. e.g: ["description"] for
    an event on the field description, defaults to None
    :type field_name: list, optional
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            _event_type = data.get("event_type", None)
            _field_name = data.get("field_name", None)

            if _event_type != event_type:
                # 202 Accepted
                return Response(status=202)

            if not field_name:
                return func(*args, **kwargs)

            if _field_name not in field_name:
                # 202 Accepted
                return Response(status=202)

            return func(*args, **kwargs)

        return wrapper

    return decorator
