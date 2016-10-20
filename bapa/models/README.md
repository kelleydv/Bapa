### Database Management
Install postgres. [Postgres.app](http://postgresapp.com/) is nice for Mac.
From a postgres shell, create databases:
```
postgres=# create database "bapa-local";
postgres=# create database "bapa-local-testing";
```
Then run the alembic manager:
```
$ python3 db.py db init    #only needs to happen if migrations/ doesn't exist
$ python3 db.py db migrate #create migration file (initially, or after updating model(s))
$ python3 db.py db upgrade #perform the migration. Do this first if cloning the repo.
```
