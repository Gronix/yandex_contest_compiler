import json as _json
import os as _os

from .utils import get_file_or_nothing as _get_file_or_nothing, \
    get_files_by_pattern as _get_files_by_pattern


def parse_contest_structure(path_to_contest):
    contest = {
        'contest_name': _os.path.split(path_to_contest)[-1],
    }
    problems = {}
    problems_dirs = [f for f in _os.scandir(path_to_contest) if f.is_dir()]

    for _problem in problems_dirs:
        samples = tests = []
        config = {}

        dirs = [f.name for f in _os.scandir(_problem) if f.is_dir()]
        if 'samples' in dirs:
            path = f"{_problem.path}/samples"
            samples = [[f'{path}/{answer[:-2]}', f'{path}/{answer}'] for answer in _get_files_by_pattern('*.a', path)]
        if 'tests' in dirs:
            path = f"{_problem.path}/tests"
            tests = [[f'{path}/{answer[:-2]}', f'{path}/{answer}'] for answer in _get_files_by_pattern('*.a', path)]
        path = f"{_problem.path}/config.json"
        if _os.path.exists(path):
            with open(path) as f:
                config = _json.load(f)

        problem = {
            'statement': _get_file_or_nothing(_problem.path, '*.tex'),
            'solution': _get_file_or_nothing(_problem.path, '*.py'),
            'samples': samples,
            'tests': tests,
            'config': config,
        }
        problems[_problem.name] = problem

    # sort problems by name
    contest['problems'] = dict(sorted(problems.items()))

    return contest
