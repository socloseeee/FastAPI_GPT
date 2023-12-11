# Как настроить BACKEND?
*инструкция любителей крабового салата*

## 1. БД (Windows/Linux)
Настрой подключение к БД postgresql в файле /backend/.env
Также необходимо установить сам Postgresql(Если не установлен)

## 2.1 Проект Windows
Переходишь в директорию FastAPI_GPT/backend и копипастишь в cmd следующее:
```commandline
python -m venv venv
cd venv
cd Scripts
activate
cd ..
cd ..
pip install -r requirements.txt
alembic init migrations
alembic revision -m "initial"
type env.py > migrations/env.py
del env.py
alembic upgrade head
alembic revision --autogenerate
alembic upgrade head
cd src
uvicorn main:app --reload
```

## 2.2 Проект Linux
Переходишь в директорию FastAPI_GPT/backend и копипастишь в cmd следующее:
```commandline
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
alembic init migrations
alembic revision -m "initial"
cp env.py migrations/env.py
rm env.py
alembic upgrade head
alembic revision --autogenerate
alembic upgrade head
cd src
uvicorn main:app --reload
```


## 3. Запуск сервера
#### 1. Перейти в директорию FastAPI_GPT/backend/src
#### 2.
Linux
Если venv не активирован:
```commandline
. venv/bin/activate
```
Запуск:
```commandline
uvicorn main:app --reload
```
Windows
Если venv не активирован:
```commandline
cd venv
cd Scripts
activate
cd ..
cd ..
```
```commandline
uvicorn main:app --reload
```
