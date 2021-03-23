virtualenv-setup:
	virtualenv .venv
virtualenv-start:
	. ./.venv/bin/activate
requirements-core:
	pip3 install -r ./requirements/requirements.txt
requirements-dev:
	pip3 install -r ./requirements/requirements.dev.txt
test:
	pytest reading_list/ --doctest-modules