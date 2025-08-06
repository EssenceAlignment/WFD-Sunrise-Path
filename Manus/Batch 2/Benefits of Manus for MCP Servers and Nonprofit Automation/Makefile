.PHONY: install test lint type-check build run clean

install:
	pip install -r app/requirements.txt

test:
	PYTHONPATH=$$PYTHONPATH:./app pytest app/tests/

test-ci:
	PYTHONPATH=$$PYTHONPATH:./app pytest -m ci_gate app/tests/

lint:
	ruff check app/

type-check:
	mypy app/

build:
	docker build -t pattern-recognition-service:latest .

run:
	docker-compose -f docker-compose.dev.yml up

clean:
	docker-compose -f docker-compose.dev.yml down
	docker system prune -f

all: install lint type-check test build

