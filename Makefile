dev:
	.venv/bin/python -m pip install -r requirements.txt
	.venv/bin/pre-commit install
	.venv/bin/python src/main.py
