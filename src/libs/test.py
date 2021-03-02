from pathlib import Path


def walk(path):
    for p in Path(path).iterdir():
        if p.is_dir():
            yield from walk(p)
            continue
        yield p.resolve()


class AutoDiscover:
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

        #         __all__.append(module_name)

    def __get_modules_from(self, path):
        return list(path.glob("**/*.py"))

    def __normalize_module_name(self, module):
        parts = module.parts
        index = parts.index(self.path.name)
        normalized = ".".join(module.parts[index::]).replace(".py", "")
        return normalized


# for p in walk(Path(".")):
#     print(p)

a = Path(__file__)
b = Path(".")


print(a.parts)

autodiscover = AutoDiscover(a.parent)
autodiscover()

# print(list(a.parent.glob('**/*.py')))
