import sys
import os
from os import listdir
from os.path import isfile, isdir, join, dirname, abspath, basename
from importlib import import_module


def __import_dir(root, name):
    path = join(dirname(abspath(__file__)), f"{name}")
    files = [f.rsplit(".py", 1)[0] for f in listdir(path) if isfile(join(path, f))]
    if len(files) == 0:
        return
    for f in files:
        import_module("".join([".", f]), f"{root}.{name}")
    sys.modules[f"{name}"] = sys.modules[f"{root}.{name}"]


def __import_file(root, name):
    name = name.rsplit(".py", 1)[0]
    import_module(f"{root}.{name}")
    sys.modules[f"{name}"] = sys.modules[f"{root}.{name}"]

# loop to handle importing deps in the wrong order
last_exception_count = None
while True:
    exception_count = 0
    top_module = basename(dirname(__file__))
    for module in sorted(listdir(dirname(__file__))):
        if module == "__init__.py" or module == "__pycache__":
            continue
        try:
            if isdir(join(top_module, module)):
                __import_dir(top_module, module)
            else:
                __import_file(top_module, module)
        except ModuleNotFoundError:
            exception_count += 1
    if exception_count == 0:
        break
    if (last_exception_count is None) or last_exception_count != exception_count:
        last_exception_count = exception_count
        continue
    break
