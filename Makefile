HOST_UID := $(shell id -u)
HOST_GID := $(shell id -g)

export HOST_UID
export HOST_GID

start:
	docker compose  -f docker-compose.yml up

start-dev:
	docker compose  -f docker-compose.yml -f docker-compose.debug.yml up

test:
	docker compose -f docker-compose.yml -f docker-compose.test.yml run --build --rm backend python manage.py test