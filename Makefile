venv:
	python -m venv venv

activate:
	. venv/Scripts/activate

install:
	pip install -r requirements.txt

run-setup:
	python setup.py

run-backend:
	python backend.py

run-frontend:
	python -m streamlit run frontend.py

test:
    pytest -v

.PHONY: test