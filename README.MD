uvicorn app.main:app --reload


alembic current 
alembic upgrade head 
alembic upgrade +1
alembic downgrade -1
alembic history
alembic heads