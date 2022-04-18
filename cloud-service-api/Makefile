help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run: env ## Arranca el flask (venv) en modo desarrollo. Server correra en: 127.0.0.1:5000
	. .venv/bin/activate && python main.py 

env: ## Configura el virtualenv
	test -d .venv || python3 -m virtualenv .venv || virtualenv .venv
	. .venv/bin/activate && pip install -Ur requirements/requirements.txt > /dev/null

dev-env: env ## Configura el virtualenv de desarrollo
	test -d .venv || python3 -m virtualenv .venv || virtualenv .venv
	. .venv/bin/activate && pip install -Ur requirements/requirements-dev.txt > /dev/null

clean: ## Elimina los ficheros basura del proyecto
	rm -rf venv
	rm -rf __pycache__
	find -iname "*.pyc" -delete
