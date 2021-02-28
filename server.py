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
# Check the signature
@check_signature(secret_key=CONFIG_OBJ.get("secret_key"))
# React on a precise event
@on_event(event_type="New_Project")
def create_project():
    """This function demonstrates how to create the project directory
    on the disk when the project is created on the prodex app."""

    # 1. Get the content of the request
    data = request.get_json()

    # 2. Define the project root directory
    projects_root = "/prod/projects"

    # In this example, we used the reference
    # for the name of the project directory
    # But you can use the name too for example.
    # 3. Get the reference of this project
    project_reference = data.get("meta").get("reference")

    # 4. Create the directory.
    path = os.path.join(projects_root, project_reference)
    os.mkdir(path)

    # 5. Always return a response.
    return Response(status=200)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
