# githasdiff

Small python script to search for changes using [fnmatch](https://docs.python.org/3/library/fnmatch.html) patterns. The principal objective is make build processes faster.

- Exits with 0 when changes are found and 1 otherwise.
- If script receives a `command`, it will be executed and exits with `command` exit code.

Inspired by [dockerfiles test script](https://github.com/jessfraz/dockerfiles/blob/master/test.sh) from **Jess Frazelle**.


## Configuration
Create a json file named `.githasdiff.json` with `include` and `exclude` patterns for each project/service/build:

```json
{
    "project_a": {
        "include": [
            "project_a/*.py"
        ],
        "exclude": [
            "project_a/extra_scripts/*.py"
        ]
    }
}
```

Global patterns can be defined in same file:

```json
{
    "include": [
        "*.py"
    ],
    "exclude": [
        "*.md"
    ]
}
```

### Observations:
- Global patterns will be always used to search for changes.
- `exclude` has priority over `include` patterns, so first exclude, then matches.
- If `include` patterns list is omitted, then script will considerate `["*"]` as `include` list pattern.

It's also possible use an env var `GITHASDIFF_FILE` to set the path to json config file.

## Run

Using if/else:

```bash
if python githasdiff.py project_a; then docker build -t project_a project_a/; else exit 0; fi
```

Using the `command` as args:

```bash
python githasdiff.py project_a docker build -t project_a project_a/
```

## Examples

Check [.githasdiff.json](.githasdiff.json) for configuration and `.travis.yml` for running.
