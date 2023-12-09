.PHONY: install migrate

venv:
	# Активация виртуальной среды
    . venv/bin/activate && \
    \
    # Установка зависимостей из requirements.txt
    pip install -r requirements.txt && \
    \
install: venv
    # Установка зависимостей из requirements.txt
    pip install -r requirements.txt

migrate:
    # Создание пользователя PostgreSQL и базы данных
    sudo -u postgres psql -c "CREATE USER postgres WITH PASSWORD 'postgres';"
    sudo -u postgres psql -c "CREATE DATABASE GPT_APP OWNER postgres;"

    # Выполнение миграции с использованием Alembic
    alembic upgrade head