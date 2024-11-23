# Insurance calculator microservice
This project is a microservice for adding tariffs and calculating insurance.

## Stack
This project uses the following stack of technologies:
1. FastAPI: - asynchronous web framework for building APIs.
2. SQLAlchemy - Python SQL toolkit and Object Relational Mapper


## Setup
Guideline for: 
- Local setup
	1. Clone repository to any machine.
	2. Install poetry:
		```bash
		pip3 install poetry
		```
	3. Install dependencies:
		```bash
		poetry install
		```
	4. Add enviroments variables
	5. Setup PostgreSQL DB
	6. Run app:
		```bash
		fastapi run src/main.py
		```
- Docker setup
	1. Build docker image
		```bash
		docker build --tag insurance-microservice .
		```
	2. Add environment variables
	3. Run docker compose
		```bash
		docker compose up -d
		```
	4. Run migrations
		```bash
		docker compose exec insurance-microservice alembic upgrade head
		```

## Environments
- Variables for PostgreSQL DB:

  - DB_HOST: Host of PostgreSQL.
  - DB_PORT: Port of PostgreSQL
  - DB_USER: Name of user that have access to database.
  - DB_NAME: Name of your database
  - DB_PASS: User password

- Variables for environment
  - ENVIRONMENT: Type of your environment
	  - local - on your machine
	  - staging - on staging server
	  - production - on production server 


## Authors
Daniil Bozhko - python software developer
