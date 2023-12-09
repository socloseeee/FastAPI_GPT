.PHONY: install migrate

venv:
	# Создание и активация виртуальной среды
	python -m venv venv
	venv\Scripts\activate

install: venv
	# Установка зависимостей из requirements.txt
	pip install -r requirements.txt

migrate:
	# Создание пользователя PostgreSQL и базы данных
	# В Linux используется sudo, а в Windows - Runas с правами администратора
	# Вместо sudo можно использовать runas на Windows, но потребуется ввод пароля администратора
	# Однако, это может не сработать в некоторых случаях.
ifeq ($(OS),Windows_NT)
	# Команды для Windows PowerShell
	# Обратите внимание, что некоторые команды могут потребовать прав администратора
	psql -U postgres -c "CREATE USER postgres WITH PASSWORD 'postgres';"
	psql -U postgres -c "CREATE DATABASE GPT_APP OWNER postgres;"
else
	# Команды для Linux
	sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD 'postgres';"
	sudo -u postgres psql -c "CREATE DATABASE GPT_APP OWNER postgres;"
endif
	# Выполнение миграции с использованием Alembic
	alembic upgrade head