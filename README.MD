## Install libraries

    pip install -r requirements.txt


## Start the server

    uvicorn app.main:app --reload

## Heroku

    heroku ps --help
    heroku ps:restart
    heroku apps:info <app_name>
    heroku run "alembic upgrade head"


## Alembic commands for database migration 

    alembic current 
    alembic upgrade head 
    alembic upgrade +1
    alembic downgrade -1
    alembic history
    alembic heads
    alembic revision --autogenerate -m "revision x"


## Generate SECRET_KEY

    openssl rand -hex 32


## Push changes

    git push origin main
    git push heroku main
    heroku run "alembic upgrade head"

## Docker

    docker build --help
    docker build -t fastapi .
    docker image ls

    docker ps
    docker run -d --name <container-name> <image-name>
    docker exec -it <container-name> bash
    docker stop <container-name>
    docker rm <container-name>
    docker rmi <image-id>

    docker run -d -p 8000:8000 fastapi 
    docker stop <container-id>
    docker rmi <image-id>
    docker rmi -f <image-id>
    docker kill <container-id>

    docker exec -it <container-name> bash

## Docker Compose

    docker-compose up --help
    docker-compose up -d
    docker-compose up -d --build
    docker-compose down
    
    docker logs <app_name>
    docker-compose run <app-name> <command>
    docker-compose run api        alembic upgrade head

    docker image tag --help
    docker image tag <container-name> <new-name>
    docker image tag <container-name> iro33/fastapi
    docker push iro33/fastapi:latest

    Run / Stop dev environment
    docker-compose -f docker-compose-dev.yml up -d
    docker-compose -f docker-compose-dev.yml down
    
    Run / Stop prod environment
    docker-compose -f docker-compose-prod.yml up -d
    docker-compose -f docker-compose-prod.yml down
    

## Pytest

    pytest -v -s
    pytest -v -s .\tests\test_users.py
    pytest --disable-warnings -v -x

## References

 - https://fastapi.tiangolo.com/
 - https://www.sqlalchemy.org/
 - https://alembic.sqlalchemy.org/en/latest/
 - https://docs.pytest.org/en/6.2.x/
