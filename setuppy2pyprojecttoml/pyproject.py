from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from copy import deepcopy
import os.path
import tomlkit


def default_requires():
    return ["setuptools >= 61.1.0"]


@dataclass
class PyProjectToml:
    @dataclass
    class BuildSystem:
        requires: List[str]# = default_requires()
        build_backend: str# = "setuptools.build_meta"

    @dataclass
    class Project:
        @dataclass
        class Author:
            name: str
            email: str

        @dataclass
        class Url:
            ...

        name: str
        version: Optional[str]
        description: Optional[str]
        readme: Optional[str]
        requires_python: Optional[str]
        license: Optional[Dict[str, Any]]
        authors: Optional[List[Author]]
        maintainers: Optional[List[Author]]
        keywords: Optional[List[str]]
        classifiers: Optional[List[str]]
        urls: Optional[List[Url]]
        # TODO entry_points
        # scripts: Scripts
        dependencies: Optional[List[str]]
        optional_dependencies: Optional[Dict[str, List[str]]]
        dynamic: Optional[List[str]]

        def as_dict(self):
            d = deepcopy(self.__dict__)
            ret = {}
            for key, value in d.items():
                key = key.replace("_", "-")
                if hasattr(value, "as_dict"):
                    value = value.as_dict()
                if value is not None:
                    ret[key] = value
            return ret


    project: Project
    build_system: BuildSystem

    @classmethod
    def from_setup(cls, kwargs: Dict[str, Any]) -> "PyProjectToml":
        return cls(
            project=PyProjectToml.Project(
                name=kwargs["name"],
                version=kwargs.get("version"),
                description=kwargs.get("description"),
                readme=None,
                requires_python=kwargs.get("python_requires"),
                license=None,
                authors=[],
                maintainers=[],
                keywords=kwargs.get("keywords"),
                classifiers=kwargs.get("classifiers"),
                urls={},  # type: ignore
                dependencies=kwargs.get("install_requires"),
                optional_dependencies=kwargs.get("extras_require"),
                dynamic=[],
            ),
            build_system=PyProjectToml.BuildSystem(
                requires=["setuptools >= 61.1.0"],
                build_backend="setuptools.build_meta",
            ),
        )

    def export(self):
        ret = {}
        if os.path.exists("pyproject.toml"):
            ret = tomlkit.load(open("pyproject.toml"))
        ret.update(self.as_dict())
        tmp_output = "pyproject.output.toml"
        tomlkit.dump(ret, open(tmp_output, "w"))

    def as_dict(self) -> Dict[str, Any]:
        d = deepcopy(self.__dict__)
        return PyProjectToml.rec(d)

    @staticmethod
    def rec(d: Dict[str, Any]):
        ret = {}
        for key, value in d.items():
            key = key.replace("_", "-")
            if hasattr(value, "as_dict"):
                value = value.as_dict()
            elif hasattr(value, "__dict__"):
                value = value.__dict__
            if value is not None:
                ret[key] = value
        return ret
