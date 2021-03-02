[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/release/python-380/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


# prodex-webhook
The webhook for the prodex application

## Setup

### What we need
* Python 3.8

(tasks are an optional feature)
* redis server (As celery Broker) (optional)
* Celery (optional)

### Setup

If you have virtualenv, you can go to step 2.
(This process can be done with pyenv too)
1. From the `prodex-webhook` directory, install the `virtualenv` package:

   ```bash
      $ pip install virtualenv
      Collecting virtualenv
      Installing collected packages: virtualenv
      Successfully installed virtualenv-16.6.0
   ```

2. Create a virtual environment named `venv`:

   ```bash
      $ virtualenv venv
      Running virtualenv with interpreter /usr/bin/python3.8
      Installing setuptools, pip, wheel...
      done.
   ```

### Source Env

1. Activate the virtual environment:

   ```bash
      $ source venv/bin/activate
      (venv)
      $
   ```

   After activation, you should see `(venv)` above your command prompt.

### Install packages

1. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install requirements.txt.

```bash
   $ (venv) pip install -r requirements.txt
```

### Launch the server

```bash
   $ (venv) python server.py
```

### Launch Celery

```bash
   $ cd src/
   $ celery -A tasks worker -l INFO
```
