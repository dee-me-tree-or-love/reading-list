venv:
	virtualenv .venv
	echo "Done, now you can activate your virtualenv via from .venv folder."
requirements-core:
	pip3 install -r ./requirements/requirements.txt
requirements-dev:
	pip3 install -r ./requirements/requirements.dev.txt
test:
	pytest reading_list/ --doctest-modules -vvv
flake8:
	flake8 --doctests --statistics --count reading_list
mypy:
	mypy reading_list/ --ignore-missing-imports --strict
isort:
	isort -p reading_list -l 99 -e reading_list