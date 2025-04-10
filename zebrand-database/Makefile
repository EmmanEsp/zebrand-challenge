init:
	test -f .env | cp .env.dist .env

up:
	docker-compose up --build --detach

create-migration:
	docker-compose run --rm dbmate_migration new ${NAME}

migration-up:
	docker-compose run --rm dbmate_migration up

migration-down:
	docker-compose run --rm dbmate_migration down

migration-status:
	docker-compose run --rm dbmate_migration status
