Step 1
=====================
[Download](https://www.python.org/downloads/release/python-31011/) and install Python 3.10.* version

Step 2
=====================
[Download](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) PostgreSQL latest version

Step 3
=====================
Launch PgAdmin and create DB with requirement name

Step 4
=====================
Create in project .env file and write in:
```
POSTGRES_USER=your_user_name
POSTGRES_PASSWORD=your_user_password
POSTGRES_SERVER=your_server_name (default localhost)
POSTGRES_PORT=your_server_port (default 5432)
POSTGRES_DB=your_db_name
JWT_SECRET_KEY=secret_key_for_jwt_token
JWT_ALGORITHM=jwt_algorithm (default HS256)
```
