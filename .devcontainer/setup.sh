python -m pip install --user --upgrade pip pip-tools
python -m piptools compile --upgrade --extra=dev -o requirements.txt pyproject.toml
python -m pip install --user -r requirements.txt
