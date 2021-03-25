virtualenv-setup:
	virtualenv .venv
requirements-core:
	pip3 install -r ./requirements/requirements.txt
requirements-dev:
	pip3 install -r ./requirements/requirements.dev.txt
test:
	pytest reading_list/ --doctest-modules -vvv
lint:
	pylint reading_list/