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
- poe validate deploys via tox, installs and checks everything. You can use it locally.

### running tests on subsets of all tests
- see [pyproject.toml/tool.pytest.ini_options/markers](../pyproject.toml) for all available test markers.
- you can use poe test -m marker name to only test some of the markers.
- a special marker is "repeat": poe test -m repeat. This repeats the last cli call and can be used to the
tests and coverage against examples (see debugging tipps below).
- also, you can filter by test name using poe test -k "<your_inclusion_pattern>".

## debugging tipps
The vscode debugger is set up to repeat the last commandline call. This means a good way to reach the code you want to debug is:
- run a commandline call that executes the code you want, eg. py -m pykasten example -n <some example that calls your code>
- this command will automatically be cached.
- run the vscode debugger. by default, it will repeat the last command, and this time it will stop at your breakpoints.
- you can repeat this as often as you want.
This also means that some form of test-driven development (or better: example-driven development) is encouraged. Write
an example of how you want the user to interface with the feature you are writing, then call this feature from the 
debugger to debug it. After you are done, you also have a basic testcase since the example will also be called
during testing.
