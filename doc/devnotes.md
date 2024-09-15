## toolchain
we assume you are using vscode. The code is toolchain-agnostic, but some of the tipps and tricks below only work in vscode.

## installing poetry and poe
to be able to use poetry and poe directly in the console,
install via pipx:
```
py -m pip install pipx
```
```
py -m pipx ensurepath 
```
```
pipx install poetry poethepoet
```

## using poetry and poe
we use poetry and poe for dev-related tasks.
for poetry, see https://python-poetry.org/docs/basic-usage/
for poe, see https://poethepoet.natn.io/index.html

some important poetry commands are:
- poetry init # to initialize repo
- poetry install --with dev # to install in dev mode
- poetry shell # activates the virtual env, "exit" to leave it
- poetry run pykasten # to run pykasten cli, alternative: "pykasten" when venv is activated
- poetry add <package> # adds dependency
- poetry add <package> --group dev # adds dependency to dev

poe commands:
- poe # shows all configured tasks
- see [pyproject.toml/tools.poe.tasks](../pyproject.toml) for all available tasks.

## testing tips
- there is no pre-commit hook (by design). Decide yourself how much testing you do before pushing.
  the cicd pipeline will execute poe validate, which checks everything.
- poe prune checks your style
- poe test checks functionality
- see [pyproject.toml/tool.pytest.ini_options/markers](../pyproject.toml) for all available test markers.
- you can use poe test -m marker name to only test some of the markers.
- a special marker is "run": poe test -m run --args <test name or example name> will run the given test or example.
- [for vscode] in test/test_run.py, you can override the default argument for "run" in the code. Then, if you run test_run with the vscode-test-debugger, you can easily debug single examples or tests. Note that in that case, coverage is disabled by launch.json, since it interferes with the debugger.
- alternatively, filter by using poe test -k "<your_inclusion_pattern>".