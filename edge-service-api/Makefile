help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

run: env ## Arranca el flask (.venv) en modo desarrollo. Server correra en: 127.0.0.1:5000
	. .venv/bin/activate && python app.py 

fake-data: ## Mete la fake data en el sql
	docker build -t fake -f FakerDockerfile .
	docker run -it --network a2_default fake

run-gunicorn: env ## Arranca el flask (.venv) en modo desarrollo. Server correra en: 127.0.0.1:5000
	. .venv/bin/activate && gunicorn -b 0.0.0.0:8080 app:app

env: ## Configura el virtualenv
	test -d .venv || python3 -m virtualenv .venv || virtualenv .venv
	. .venv/bin/activate && pip install -Ur requirements/requirements.txt > /dev/null

dev-env: env ## Configura el virtualenv de desarrollo
	. .venv/bin/activate && pip install -Ur requirements/requirements-dev.txt > /dev/null

freeze: clean env
	. .venv/bin/activate && pip freeze > requirements/requirements.txt

freeze-dev: clean dev-env
	. .venv/bin/activate && pip freeze > requirements/requirements-dev.txt
    
test: dev-env
	. .venv/bin/activate && pytest --cov-report term-missing --cov=./ -s -vv

clean: ## Elimina los ficheros basura del proyecto
	rm -rf .pytest_cache .venv
	find -iname "*.pyc" -delete
	find -type d -iname "__pycache__" -delete

simulate-camera-event:
	mosquitto_pub -h test.mosquitto.org -p 1883 -q 2 -t "gesys/edge/camara" -m '{"matricula": "HH12D23", "id_estacio": "VG1"}'

simulate-barrier-listener:
	mosquitto_sub -h test.mosquitto.org -p 1883 -q 2 -t "gesys/estaciones/VG1/camara" 

simulate-averias0:
	mosquitto_pub -h test.mosquitto.org -p 1883 -q 2 -t "gesys/edge/puntoCarga/averia" -m '{"idPuntoCarga": 2, "averia": 0}'
	
simulate-averias1:
	mosquitto_pub -h test.mosquitto.org -p 1883 -q 2 -t "gesys/edge/puntoCarga/averia" -m '{"idPuntoCarga": 2, "averia": 1}'
	
simulate-averias2:
	mosquitto_pub -h test.mosquitto.org -p 1883 -q 2 -t "gesys/edge/puntoCarga/averia" -m '{"idPuntoCarga": 2, "averia": 2}'
	
simulate-averias3:
	mosquitto_pub -h test.mosquitto.org -p 1883 -q 2 -t "gesys/edge/puntoCarga/averia" -m '{"idPuntoCarga": 2, "averia": 3}'
	
simulate-averias4:
	mosquitto_pub -h test.mosquitto.org -p 1883 -q 2 -t "gesys/edge/puntoCarga/averia" -m '{"idPuntoCarga": 2, "averia": 4}'
	
simulate-bateria-vehiculo:
	mosquitto_pub -h test.mosquitto.org -p 1883 -q 2 -t "gesys/edge/vehiculo" -m '{"battery": 0, "matricula":"HH12D23"}'
	
