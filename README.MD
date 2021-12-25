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