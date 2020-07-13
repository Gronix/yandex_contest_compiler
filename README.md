# Yandex.Contest compiler
Compiling archive with competition for Yandex.Contest from sources.

For Python3.6+

## Usage

Inside repo directory run module like this:

```
python -m contest -p </path/to/contest/source> -c </path/to/cfg.json> -d </destination/path> -n <contest_name>
```

Keys

```
usage: __main__.py [-h] -p PATH -c CONFIG [-d DEST] [-t TEMPLATES] [-n NAME]
                   [-v]

optional arguments:
  -h, --help                            show this help message and exit
  -p PATH, --path PATH                  path to contest source
  -c CONFIG, --config CONFIG            path to user config
  -d DEST, --dest DEST                  path to contest archive destination
  -t TEMPLATES, --templates TEMPLATES   path to templates
  -n NAME, --name NAME                  explicit set contest name 
                                        (dirname is used if argument omitted)
  -v, --verbose                         be more verbosity
```

## Examples

* Example of sources see in:
    > ./contest/tests/raw_contests

* Example of compiled contest see in: 
    > ./contest/tests/compiled_contest

* Example of solution with checking for yours samples and tests:
    > ./solution_with_checker_example.py

* Example of creating contest (from test sources):

    Inside directory with contest_compiler repository (preferable to use absolute path)
    ```
    python3.7 -m contest -p tests/raw_contests/test-contest -c configs/cfg.json -d tests/compiled_contests -n test1
    ```

## Upload to Yandex.Contest
In Admin interface:
1. Click to the "Add Competition" button 
2. Select "YANDEX" contest format
3. Click to the "Select file" button
4. Select compiled archive
5. After some time contest will be created


## Notes:

* After uploading of competition into Yandex.Contest you need to check the order of problems 