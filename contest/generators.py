import json as _json
import os as _os
from string import Template as _Template

import typing as _typing

from .utils import get_abc_upper as _get_abc_upper


def generate_config(contest_name, user_config, contest_structure) -> _typing.Dict[str, _typing.Union[str, dict]]:
    if isinstance(user_config, str) and _os.path.exists(user_config):
        with open(user_config) as f:
            user_config = _json.load(f)
    if not isinstance(user_config, dict):
        user_config = {}

    config = {
        **user_config,
        'contest_name': contest_name or user_config.get('contest_name', contest_structure.get('contest_name', '')),
        'problems': {}
    }

    abc = _get_abc_upper(len(contest_structure['problems']))
    for code_name, (problem_name, problem_spec) in zip(abc, contest_structure['problems'].items()):
        config['problems'][code_name] = {'problem_title': problem_name, **problem_spec}
        config['problems'][code_name]['config'] = {**user_config, **config['problems'][code_name].get('config', {})}

    return config


def generate_tex_from_body(problem: dict, templates_dir: str) -> str:
    tex_body = samples = ''
    if problem['statement']:
        with open(f"{templates_dir}/statement.tex") as f1, open(problem['statement']) as f2:
            template = _Template(f1.read())
            tex_body = f2.read()
    if problem['samples']:
        samples = []
        for sample, answer in problem['samples']:
            with open(sample) as f1, open(answer) as f2:
                samples.append(f"{{{f1.read()}}}{{{f2.read()}}}")
        samples = '\exmp'.join(samples)
    statement = template.substitute(
        problem_title=problem.get('problem_title', 'Unnamed'),
        limit_time=problem['config']['limit_time'],
        limit_memory=problem['config']['limit_memory'],
        body=tex_body,
        examples=samples,
    )
    return statement


def generate_summary_statement(statements: _typing.List[str], templates_dir: str) -> str:
    with open(f'{templates_dir}/statements_summary.tex') as f:
        summary_template = _Template(f.read())
    return summary_template.substitute(problems_statements='\n'.join(statements))
