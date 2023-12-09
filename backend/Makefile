.PHONY: install migrate

# Подключаем файл .env
include .env

venv:
	# Создание виртуальной среды
ifeq ($(OS),Windows_NT)
	# Команды для Windows
	python -m venv venv
else
	# Команды для Linux
	python3 -m venv venv
endif

activate_venv:
ifeq ($(OS),Windows_NT)
	# Активация виртуальной среды на Windows
	venv\Scripts\activate && pip install -r requirements.txt
else
	# Активация виртуальной среды на Linux
	. venv/bin/activate && pip install -r requirements.txt
endif

install: venv activate_venv

create_database:
	# Создание пользователя PostgreSQL и базы данных
ifeq ($(OS),Windows_NT)
	# Команды для Windows
	psql -U $(DB_USER) -c "CREATE USER $(DB_USER) WITH PASSWORD '$(DB_PASS)';"
	psql -U $(DB_USER) -c "CREATE DATABASE $(DB_NAME) OWNER $(DB_USER);"
else
	# Команды для Linux
	sudo -u postgres psql -c "CREATE USER $(DB_USER) WITH PASSWORD '$(DB_PASS)';"
	sudo -u postgres psql -c "CREATE DATABASE $(DB_NAME) OWNER $(DB_USER);"
endif

migrate: create_database
	# Выполнение миграции с использованием Alembic
	alembic upgrade head
