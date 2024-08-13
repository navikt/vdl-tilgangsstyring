
SHELL = /bin/bash
.DEFAULT_GOAL = install

PY = ./.venv/bin/python -m
PY_LOCK = ./.venv-lock/bin/python -m

.PHONY: install ## install requirements in virtual env
install:
	rm -rf .venv
	python3.11 -m venv .venv && \
		$(PY) pip install --upgrade pip && \
		$(PY) pip install -r requirements-lock.txt -r requirements-dev.txt

_lock-file:
	python3.11 -m venv .venv-lock && \
		$(PY_LOCK) pip install --upgrade pip && \
		$(PY_LOCK) pip install -r requirements.txt && \
		$(PY_LOCK) pip freeze > requirements-lock.txt
	rm -rf .venv-lock

.PHONY: lock-file ## Create pip-lockfile and install its dependencies
lock-file: _lock-file install
