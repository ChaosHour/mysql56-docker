.PHONY: build up down down_all start_repl

build:
	docker-compose build

up:
	docker-compose up -d --build --wait
	sleep 10
	make start_repl

down:
	docker-compose down

down_all:
	docker-compose down -v --rmi all --remove-orphans

start_repl:
	zsh -c ./start_repl.sh