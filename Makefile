.PHONY: build up down clean_networks clean_volumes

build:
	docker-compose build

up:
	docker-compose up -d --build --wait

down:
	docker-compose down

clean_volumes:
	docker-compose down -v --remove-orphans

clean_networks:
	docker network prune -f