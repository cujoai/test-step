# Copyright (c) 2026 CUJO LLC
setup-venv:
	venv/bin/python3 -m virtualenv venv

config: venv
	venv/bin/pip install --upgrade pip
	venv/bin/pip install -e ".[test]"
	venv/bin/pip freeze

build: config
	venv/bin/pip install --upgrade setuptools wheel twine
	venv/bin/python3 setup.py sdist bdist_wheel

publish-local: build
	twine upload dist/*
