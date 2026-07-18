

after api is built : github actions


linkedin me y my approach failed first which is image log , now what i am using , how i can do better 

1. 
venv : python -m venv .venv // begins with dot (naming pattern)
    source .venv/bin/activate  // to run
    deactivate  // to ...

2.
installation from diff levels : dev , prod
    pip install -r requirements/dev.txt

3.
in linux .gitignore is case sensitive

4.
best scalable architecture acc to service not mvc(dump all model at one place)

5.
alembic is similar to goose for python : DB migration (more on that later)
-i am creating Db in root to diff it from being part of both ends
-also the docker_compose will be on root will be

6. pydantic settings is used to fecth and create an instace of .env settings, which loadas at the start of server 

7. jwt auth

8. migration :
- i dont need an external .venv , i can just use alembic which is package provided along side sqlachmely in backend, but i am keeping  it on root to show its Database not Backend..
8.1 alembic init migrations  => will make alembic.ini
8.2 set it for using venv instead of global repos
```python
import sys
from os import path

# 1. Tell Python to look inside the backend folder for imports
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))) + "/backend")
```
8.3 Goose is a language-agnostic migration tool where you write the raw, explicit CREATE TABLE and DROP TABLE SQL queries yourself inside separate up.sql and down.sql blocks.

Alembic does things completely differently. Because it is built specifically for SQLAlchemy, it defaults to an automatic state-matching approach called --autogenerate.

8.4 add sys path at top to tell python where the venv is since i am separating it from backend

8.5 set sql_url in .ini dynamically from migrations/env.py 

8.6 get model data to be included so that the migrations can be auto genrate

8.7 make sure the postgre service is running then , generate 
    `alembic revision --autogenerate -m "create_users_table"`

8.8 `alembic upgrade head` this will upgrage migration one step

8.# info it stores an additianal table(alembic_version) which keeps the current db migration version , which maches the migration file serial id


 





