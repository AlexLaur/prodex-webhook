# Tasks

Place any `.py` files here, in order to create tasks for the webhook. With tasks, the main instance of the webhook will never be busy by long process.


## Initialise Celery
***

from `src` directory, execute :

```bash
$ celery -A tasks worker -l INFO
```

## Create a task
***

In each of `.py` files, your need to import the celery application

```python
from . import celery_app
```

In order to create a task, you just need to create a function and decorate it like this:

```python
@celery_app.task
def my_task():
    ...
```

And then, Celery will automatically discover your task.

Use the task from the webhook:

```python
from task.my_py_file import my_task
# simple exemple
my_task.delay()
# with args
my_task.delay(var1, var2, ...)
```