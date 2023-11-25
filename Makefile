.PHONY: build up down clean_networks clean_volumes start_repl

build:
	docker-compose build

up:
	docker-compose up -d --build --wait
	sleep 10
	make start_repl

down:
	docker-compose down

clean_volumes:
	docker-compose down -v --remove-orphans

clean_networks:
	docker network prune -f

start_repl:
	zsh -c ./start_repl.sh