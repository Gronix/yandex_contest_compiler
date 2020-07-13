from argparse import ArgumentParser as _ArgumentParser, Namespace as _Namespace
from collections import namedtuple as _namedtuple
from glob import glob as _glob
import os as _os
import string as _string
import tempfile as _tempfile
import zipfile as _zipfile

import typing as _typing


def parse_args():
    parser = _ArgumentParser()
    parser.add_argument('-p', '--path', required=True, help='path to contest source')
    parser.add_argument('-c', '--config', required=True, help='path to user config')
    parser.add_argument('-d', '--dest', help='path to contest archive destination')
    parser.add_argument('-t', '--templates', default='templates/default', help='path to templates')
    parser.add_argument('-n', '--name', required=False, help='explicit set contest name (dirname is used if argument omitted)')
    parser.add_argument('-v', '--verbose', action='store_true', help='be more verbosity')
    return normalize_args(parser.parse_args())


def normalize_args(args: _Namespace):
    ArgsType = _namedtuple('NormalizedArgs', ['path', 'dest', 'config', 'templates', 'name'])
    cur_path = get_cur_dir_path()
    prepared_args = {}

    for arg in ('path', 'config', 'templates'):
        arg_value = getattr(args, arg)
        if arg_value.startswith('/'):
            prepared_args[arg] = arg_value
        else:
            prepared_args[arg] = f'{cur_path}/{arg_value}'

    if not args.dest:
        prepared_args['dest'] = f'{prepared_args["path"]}/{_os.path.split(prepared_args["path"])[-1]}.zip'
    elif not args.dest.startswith('/'):
        prepared_args['dest'] = f'{cur_path}/{args.dest}'
    else:
        prepared_args['dest'] = args.dest

    if not prepared_args['dest'].endswith('.zip'):
        archive_name = f'{args.name}.zip' if args.name else f'{_os.path.split(prepared_args["path"])[-1]}.zip'
        prepared_args['dest'] = f'{prepared_args["dest"]}/{archive_name}'

    prepared_args['name'] = args.name

    return ArgsType(**prepared_args)


def create_dummy_file(extension) -> _tempfile.NamedTemporaryFile:
    return _tempfile.NamedTemporaryFile(suffix=extension, delete=False)


def create_temp_dir() -> _tempfile.TemporaryDirectory:
    return _tempfile.TemporaryDirectory()


def create_dirs_and_return_path(path) -> str:
    _os.makedirs(path)
    return path


def get_file_or_nothing(path, glob_pattern) -> _typing.Union[str, None]:
    prev_path = get_cur_dir_path()
    _os.chdir(path)
    file = (list(_glob(glob_pattern)) or [None])[0]
    if file is not None:
        file = f"{path}/{file}"
    _os.chdir(prev_path)
    return file


def get_files_by_pattern(pattern: str, path: _typing.Optional[str] = None):
    prev_path = None
    if path is not None:
        prev_path = get_cur_dir_path()
        _os.chdir(path)

    files = _glob(pattern)

    if prev_path is not None:
        _os.chdir(prev_path)
    return files


def get_abc_upper(n) -> _typing.List[str]:
    abc = list(_string.ascii_uppercase)
    if len(abc) < n:
        abc.extend([f"{abc[i // len(abc)]}{abc[i % len(abc)]}" for i in range(n - len(abc))])
    elif len(abc) > n:
        abc = abc[:n]
    return abc


def pack_content_of_dir(dir_path, archive_path, current_name):
    def zipdir(path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in _os.walk(path):
            for file in files:
                if not file.endswith('.zip'):
                    ziph.write(_os.path.join(root, file))
    if not archive_path.endswith('.zip'):
        archive_path = f'{archive_path}/{current_name}.zip'

    print('Competition archive stored at path:', archive_path, sep='\n')
    prev_path = get_cur_dir_path()
    _os.chdir(dir_path)
    with _zipfile.ZipFile(archive_path, 'w', _zipfile.ZIP_DEFLATED) as zip_archive:
        zipdir('./', zip_archive)
    _os.chdir(prev_path)


def get_cur_dir_path():
    return _os.path.split(__file__)[0]
