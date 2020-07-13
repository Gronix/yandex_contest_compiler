import shutil

from .builders import *
from .compilers import compile_configs
from .generators import *
from .parsers import parse_contest_structure
from .utils import parse_args, pack_content_of_dir


args = parse_args()
contest_src = parse_contest_structure(args.path)

config = generate_config(args.name, args.config, contest_src)
statements = []
contest = build_correct_contest_structure()
try:
    for problem_code, problem in config['problems'].items():
        problem_structure = build_problem_structure(problem_code, contest)

        # create problem statement
        statement_tex = generate_tex_from_body(problem, args.templates)
        statements.append(statement_tex)
        tex_sourcefile = f"{problem_structure['statements-ru']}/tex/statement.tex"
        with open(tex_sourcefile, 'w') as f:
            f.write(statement_tex)

        # copy problem solution
        shutil.copy(problem['solution'], problem_structure['solutions'])

        # copy problem samples and tests
        i = 0
        for examples_part in ('samples', 'tests'):
            for i, (j, (example, answer)) in enumerate(enumerate(problem[examples_part]), i+1):
                problem[examples_part][j].append(i)
                shutil.copy(example, f"{problem_structure['tests']}/{i:0>3}")
                shutil.copy(answer, f"{problem_structure['tests']}/{i:0>3}.a")

    # create xml and json contest configs
    compile_configs(config, contest['base'], args.templates)

    # create summary statement
    statement_summary = generate_summary_statement(statements, args.templates)
    with open(f"{contest['statements']}/statement.tex", 'w') as f:
        f.write(statement_summary)

    # create zip archive with contest
    pack_content_of_dir(contest['base'], args.dest, config['contest_name'])

finally:
    # cleanup
    contest['_tmp_dir_obj'].cleanup()
