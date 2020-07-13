import os as _os
import tempfile as _tempfile
import typing as _typing

from .utils import create_temp_dir as _create_temp_dir, \
                   create_dirs_and_return_path as _create_dirs_and_return_path


def build_correct_contest_structure() -> _typing.Dict[str, _typing.Union[str, _tempfile.TemporaryDirectory]]:
    base_dir = _create_temp_dir()

    contest = {
        '_tmp_dir_obj': base_dir,
        'base': base_dir.name,
        'problems': _create_dirs_and_return_path(f"{base_dir.name}/problems"),
        'statements': _create_dirs_and_return_path(f"{base_dir.name}/statements/ru/tex")
    }
    return contest


def build_problem_structure(problem_code: str, contest: _typing.Dict[str, str]) -> _typing.Dict[str, str]:
    base_path = f"{contest['problems']}/{problem_code}"
    problem = {
        'base': base_path,
        'solutions': _create_dirs_and_return_path(f"{base_path}/solutions"),
        'statements-ru': _create_dirs_and_return_path(f"{base_path}/statements/ru"),
        'tests': _create_dirs_and_return_path(f"{base_path}/tests"),
    }
    _os.makedirs(f"{problem['statements-ru']}/tex")
    # _os.makedirs(f"{problem['statements-ru']}/html")

    return problem
