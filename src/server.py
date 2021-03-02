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

from flask import Flask, Response, request, render_template

from utils.decorators import check_signature, on_event
from utils import utils

from tasks import projects_tasks


SCRIPT_PATH = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(SCRIPT_PATH, "config", "conf.yml")
CONFIG_OBJ = utils.load_config_file(path=CONFIG_FILE)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """Go to localhost:5000 to see a message"""
    return render_template("index.html")


@app.route("/echo", methods=["POST"])
def echo():
    """Display the data from the request"""
    print(request.get_json())
    return Response(status=200)


# Example

# Endpoint definition
@app.route("/project/new", methods=["POST"])
# Check the signature (Optional but recommended)
@check_signature(secret_key=CONFIG_OBJ.get("secret_key"))
# React on a precise event (Optional)
@on_event(event_type="New_Project")
def create_project():
    """This function demonstrates how to create the project directory
    on the disk when the project is created on the prodex app."""

    # 1. Get the content of the request
    data = request.get_json()

    # 2. Execute the asynchronous task
    projects_tasks.create_project_folder.delay(request_data=data)

    # Always return a response.
    return Response(status=200)


if __name__ == "__main__":
    host = os.environ.get("HOST", "127.0.0.1")
    debug = os.environ.get("DEBUG", 1)
    use_reloader = os.environ.get("RELOADER", 1)

    app.run(debug=debug, use_reloader=use_reloader, host=host)
