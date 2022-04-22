linter:
	@test -d .venv || python3 -m virtualenv .venv || virtualenv .venv
	@. .venv/bin/activate && pip install flake8 > /dev/null && flake8 --statistics

