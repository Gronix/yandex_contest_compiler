import json as _json
import os as _os
from string import Template as _Template


def _compile_config_json(config, templates_dir):
    def compile_examples(problem):
        i, examples = 1, {}
        if problem['samples']:
            examples[str(i)] = {'from': problem['samples'][0][-1], 'to': problem['samples'][-1][-1], 'example': True}
            i += 1
        if problem['tests']:
            examples[str(i)] = {'from': problem['tests'][0][-1], 'to': problem['tests'][-1][-1], 'example': False}
        return _json.dumps(examples)
    with open(_os.path.join(templates_dir, 'problem.json')) as f1, \
            open(_os.path.join(templates_dir, 'meta.json')) as f2:
        problem_template = _Template(f1.read())
        config_template = _Template(f2.read())
    problems = []
    problem_codes = ', '.join((f'"{code}"' for code in config['problems']))
    for problem in config['problems'].values():
        problems.append(problem_template.substitute(
            problem_title=problem['problem_title'],
            author=problem['config']['author'],
            test_sets=compile_examples(problem),
            solution=_os.path.split(problem['solution'])[-1],
            limit_time=problem['config']['limit_time'],
            limit_memory=problem['config']['limit_memory'],
        ))
    json_config = config_template.substitute(
        contest_name=config['contest_name'],
        duration='' if not config['duration'] else '"duration": {dur},'.format(dur=config['duration']),
        problem_codes=problem_codes,
        problems=', '.join(problems),
        registration=config['registration'],
    )
    return json_config


def _compile_config_xml(config, templates_dir):
    def compile_examples(problem):
        example_template = _Template("""
        <test-sets>
            <key>$key</key>
            <value>
                <from>$from_</from>
                <to>$to</to>
                <example>$is_sample</example>
            </value>
        </test-sets>""")
        i, examples = 1, []
        if problem['samples']:
            examples.append(example_template.substitute(key=i,
                                                        from_=problem['samples'][0][-1],
                                                        to=problem['samples'][-1][-1],
                                                        is_sample='true'))
            i += 1
        if problem['tests']:
            examples.append(example_template.substitute(key=i,
                                                        from_=problem['tests'][0][-1],
                                                        to=problem['tests'][-1][-1],
                                                        is_sample='false'))
        return '\n'.join(examples)
    with open(_os.path.join(templates_dir, 'problem.xml')) as f1, \
            open(_os.path.join(templates_dir, 'meta.xml')) as f2:
        problem_template = _Template(f1.read())
        config_template = _Template(f2.read())
    problems = []
    problem_codes = '\n'.join((f'<problem-names>{code}</problem-names>' for code in config['problems']))
    for problem in config['problems'].values():
        problems.append(problem_template.substitute(
            problem_title=problem['problem_title'],
            author=problem['config']['author'],
            test_sets=compile_examples(problem),
            solution=_os.path.split(problem['solution'])[-1],
            limit_time=problem['config']['limit_time'],
            limit_memory=problem['config']['limit_memory'],
        ))
    xml_config = config_template.substitute(
        contest_name=config['contest_name'],
        duration='' if not config['duration'] else f"<duration>{config['duration']}</duration>",
        problem_codes=problem_codes,
        problems=', '.join(problems),
        registration=config['registration'],
    )
    return xml_config


def compile_configs(config, store_path, templates_dir):
    config_json = _compile_config_json(config, templates_dir)
    config_xml = _compile_config_xml(config, templates_dir)
    with open(f'{store_path}/meta.json', 'w') as json_file, open(f'{store_path}/meta.xml', 'w') as xml_file:
        json_file.write(config_json)
        xml_file.write(config_xml)
