# backend сервиса аутентификации проекта nous
-------------------------

CPython version >= 3.8

### Локальная установка:
- Создание базы:
    ```
    $ sudo -u postgres psql
    CREATE DATABASE nous_auth ENCODING 'UTF-8'
    LC_COLLATE = 'en_US.UTF-8' LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE template0;
    # Создание пользователя
    CREATE USER nous WITH PASSWORD 'nous123';

    # Выдача прав на базу
    GRANT ALL PRIVILEGES ON DATABASE "nous_auth" TO nous;
    ALTER USER nous CREATEDB;
  ```

- Установка зависимостей:
    ```
    $ pip install -r requirements.txt
    ```