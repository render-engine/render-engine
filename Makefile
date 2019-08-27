init:
	pip install pipenv
	pipenv install --dev

test:
	pipenv run python -m pytest
