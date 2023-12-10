# Как настроить BACKEND?
*инструкция любителей крабового салата*

## 1. БД
Настрой подключение к БД postgresql в файле /backend/.env
Также необходимо установить сам Postgresql(Если не установлен)

## 2.1 Makefile(Linux)

```commandline
make install
```

```commandline
make migrate
```

## 2.2 Windows(configuration)
1) Перейти в диркеторию ```cd backend```
2) Выполнить следующие инструкции:
```commandline
pythoh -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
```
3) Проинициировать миграции
```commandline
alembic init migrations
alembic revision -m
 "initial"  
alembic revision --
autogenerate
alembic upgrade head
```


## 3. Запуск сервера
#### 1. Перейти в директорию /backend/src
#### 2.
Linux
```commandline
. venv/bin/activate && uvicorn main:app --reload
```
Windows
```commandline
.venv/Scripts/activate && uvicorn main:app --reload
```
