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
alembic revision -m "initial"  
alembic revision --autogenerate
alembic upgrade head
```
4) Содержимое backend/migratiins/env.py файл заменить на:
```python
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

import os
import sys

sys.path.append(os.path.join(sys.path[0], 'src'))

from src.config import DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASS
from src.operations.models import metadata as metadata_operations

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

section = config.config_ini_section
config.set_section_option(section, "DB_HOST", DB_HOST)
config.set_section_option(section, "DB_PORT", DB_PORT)
config.set_section_option(section, "DB_USER", DB_USER)
config.set_section_option(section, "DB_NAME", DB_NAME)
config.set_section_option(section, "DB_PASS", DB_PASS)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = [metadata_operations]

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
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
