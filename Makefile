.PHONY: build up down

build:
	docker-compose build

up:
	docker-compose up -d --build --wait

down:
	docker-compose down