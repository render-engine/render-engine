python -m pip install --user --upgrade pip
python -m pip install --user pip-tools
python -m piptools compile --upgrade -o requirements.txt pyproject.toml
python -m pip install --user -r requirements.txt
python -m pip install -e .
pre-commit install
