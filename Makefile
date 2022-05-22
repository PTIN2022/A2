linter:
	@test -d .venv || python3 -m virtualenv .venv || virtualenv .venv
	@. .venv/bin/activate && pip install flake8 > /dev/null && flake8 --statistics

cloud:
	docker-compose -f ./docker-compose-cloud.yml down -v
	docker-compose -f ./docker-compose-cloud.yml up -d --build

cloud-logs:
	docker-compose -f ./docker-compose-cloud.yml logs -f

edge:
	docker-compose -f ./docker-compose-edge.yml down -v
	docker-compose -f ./docker-compose-edge.yml up --build

edge-logs:
	docker-compose -f ./docker-compose-edge.yml logs -f
