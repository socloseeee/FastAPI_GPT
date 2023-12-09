# Как настроить BACKEND?
*инструкция любителей крабового салата*

## 1. БД
Настрой подключение к БД postgresql в файле /backend/.env

## 2. Makefile
```commandline
make install
```

```commandline
make migrate
```

## 3. Запуск сервера
#### 1. Перейти в директорию /backend/src
#### 2.
```commandline
uvicorn main:app --reload
```
