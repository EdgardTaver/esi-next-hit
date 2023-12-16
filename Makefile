venv:
	python -m venv venv

activate:
	. venv/Scripts/activate

install:
	pip install -r requirements.txt

setup: venv activate install

test:
    pytest -v

.PHONY: test