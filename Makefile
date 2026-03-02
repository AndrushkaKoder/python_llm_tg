COMPOSE = docker compose

up:
	${COMPOSE} up -d --build --remove-orphans

down:
	${COMPOSE} down

restart: down up


