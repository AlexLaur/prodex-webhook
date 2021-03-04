# -*- coding: utf-8 -*-
#
# - __init__ -
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
import importlib
from pathlib import Path

from celery import Celery

__all__ = []  # Used to store all tasks which have been found

# Define celery application
celery_app = Celery(__name__)

celery_app.conf.broker_url = os.environ.get(
    "CELERY_BROKER", "redis://localhost:6379"
)
celery_app.conf.result_backend = os.environ.get(
    "CELERY_BACKEND", "redis://localhost:6379"
)

# Debub task
@celery_app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))


# AUtodiscover all tasks
class AutoDiscover(object):
    """
    This class search modules from a given path recursively.
    It searches all the modules and run an `import_module` for each.
    :param path: `pathlib.Path` object
    :param pattern: str object - (Optional)
    :return: None
    How to use:
        autodiscover = AutoDiscover(path="path/to/models", pattern="model")
        autodiscover()
    """

    def __init__(self, path, pattern=None):
        self.path = path
        self.pattern = pattern

    def __call__(self):
        return self.__execute(path=self.path, pattern=self.pattern)

    def __execute(self, path, pattern):
        modules = self.__get_modules_from(path)

        for module in reversed(modules):
            if module.name.startswith("_"):
                continue

            if module.is_file() and module.match(pattern or "*"):
                module_name = self.__normalize_module_name(module)

                importlib.import_module(module_name)

                __all__.append(module_name)

    def __get_modules_from(self, path):
        return list(path.glob("**/*.py"))

    def __normalize_module_name(self, module):
        parts = module.parts
        index = parts.index(self.path.name)
        normalized = ".".join(module.parts[index::]).replace(".py", "")
        return normalized


# Discovers tasks for celery
path = Path(__file__).parent
AutoDiscover(path=path)()
