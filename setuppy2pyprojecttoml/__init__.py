from unittest import mock
import os
from typing import Any, Dict

from setuppy2pyprojecttoml.pyproject import PyProjectToml


def main():
    assert os.path.exists("setup.py"), "setup.py does not exists."
    os.environ["PYTHONPATH"] = "."

    with mock.patch("setuptools.setup") as mocked_obj:
        import setup  # type: ignore
        call_kwargs = mocked_obj.call_args.kwargs  # type: Dict[str, Any]
        pyproject = PyProjectToml.from_setup(call_kwargs)
        pyproject.export()


__version__ = "0.1.0"
