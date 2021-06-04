<!-- markdownlint-disable-next-line no-trailing-punctuation -->
# Reading-List: CLI :books:

Manage your links to read using this CLI tool!  

> Disclaimer: it's a work in progress, but do stay tuned ;)

## Usage

<!-- To be defined -->

## Development

### Pre-Requisites

- [`Python 3.7+`](https://www.python.org/downloads/)
- [`make`](https://www.gnu.org/software/make/)

### Utilities

For a list of available utility scripts for this project,
check the [`Makefile`](./Makefile) contents.

#### Setup virtual environment

```bash
$ make virtualenv-setup
virtualenv .venv
created virtual environment ...
$ . .venv/bin/activate # or appropriate command for your system
```

#### Install requirements

```bash
$ make requirements-core # installs the main project requirements
$ make requirements-dev # installs the development dependencies
```

#### Testing

```bash
$ make test
pytest reading_list/ --doctest-modules -vvv
...
```

#### Lint & Type Checking

```bash
$ make lint # run the python linter
$ make mypy # run the mypy type checker
```
