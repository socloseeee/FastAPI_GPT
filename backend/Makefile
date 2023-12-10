.PHONY: install migrate

# Подключаем файл .env
include .env

venv:
	# Создание виртуальной среды
	python3 -m venv venv
	. venv/bin/activate && pip install -r requirements.txt

create_database:
	# Создание пользователя PostgreSQL и базы данных
	sudo -u postgres psql -c "CREATE USER $(DB_USER) WITH PASSWORD '$(DB_PASS)';"
	sudo -u postgres psql -c "CREATE DATABASE $(DB_NAME) OWNER $(DB_USER);"

migrate: create_database
	# Выполнение миграции с использованием Alembic
	alembic init migrations
    alembic revision -m "initial"
    alembic revision -- autogenerate
    alembic upgrade head

install: venv migrate
