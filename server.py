# -*- coding: utf-8 -*-
#
# - server -
#
# The main application of the prodex webhook.
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
import yaml

from flask import Flask, Response, request

from utils.decorators import check_signature
from utils import utils


SCRIPT_PATH = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(SCRIPT_PATH, "config", "conf.yml")
CONFIG_OBJ = utils.load_config_file(path=CONFIG_FILE)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Go to localhost:5000 to see a message"""

    return ("This is a website.", 200, None)


@app.route("/api/print", methods=["POST"])
@check_signature(secret_key=CONFIG_OBJ.get("secret_key"))
def print_test():
    """ Send a POST request to localhost:5000/api/print with a JSON body."""
    print(request.get_json())
    return Response(status=200)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
