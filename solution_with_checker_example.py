def checker():
    import pathlib
    if pathlib.Path.home().name not in __file__:
        solve()
        return

    import os
    if int(os.environ.get('IS_TEST_RUN', '0')):
        solve()
        return

    import collections, glob, subprocess, sys

    TestType = collections.namedtuple('TestType', ['test_data', 'answer'])
    curr_path = os.path.dirname(os.path.realpath(__file__))
    test_cases = {
        'samples': [],
        'tests': [],
    }

    for tests_part, container in test_cases.items():
        for sample_answer_path in glob.glob(f'{curr_path}/{tests_part}/*.a'):
            with open(sample_answer_path[:-2]) as test_file, \
                    open(sample_answer_path) as answer_file:
                container.append(TestType(test_file.read(), answer_file.read()))

    i = 0
    all_tests_passed = True
    for tests_part in test_cases:
        for i, test in enumerate(test_cases[tests_part], i+1):
            p = None
            try:
                p = subprocess.Popen([sys.executable, __file__],
                                     stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                     env={**os.environ.copy(), 'IS_TEST_RUN': '1'},
                                     encoding='utf8')
                output, exit_code = p.communicate(test.test_data)
                assert not exit_code, f"Program terminated with {exit_code} on test №{i} in {tests_part} section"
                assert output == test.answer, f"Failed on test №{i} in {tests_part} section:\n" \
                                              f"{'-'*10}\n{output}\n{'-'*10}\n" \
                                              f"But expected:\n{'-'*10}\n{test.answer}\n{'-'*10}\n"
            except AssertionError as e:
                all_tests_passed = False
                print(e)
            finally:
                if p:
                    p.kill()
    if all_tests_passed:
        print('OK')


def solve():
    # here is your solution code
    pass


if __name__ == '__main__':
    checker()
