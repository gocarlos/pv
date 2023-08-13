up:
	docker-compose -f docker-compose.yml up

pull:
	docker-compose pull

restart:
	docker-compose -f docker-compose.yml down && docker-compose -f docker-compose.yml up

build:
	docker-compose -f docker-compose.yml up --build --remove-orphans

down:
	docker-compose -f docker-compose.yml down

bash:
	docker exec -it asfd bash
