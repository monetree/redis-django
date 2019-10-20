# Steps to run this app locally with mongodb

1. install redis (`https://redis.io/`)
2. install mongodb (`https://www.mongodb.com/`)
3. create database with named `dummy` in mongodb
4. dump the data `comments.csv` or `comments.json` into db using `mongoexport --db=dummy --collection=comments --out=comments.json` command

5. install requiremets using `pip install -r requirements.txt` (You can use virtualenv also as i am using)
6. run `python manage.py migrate`
7. run `python manage.py` in current directory
8. in browser run `http://127.0.0.1:8000/mongo/users/` (you can pass `?no_cache=yes` parameter with url if you don't want cached data. I explained about this inside code )
9. I created one extra api using Raw mongo query `http://127.0.0.1:8000/pymongo/texture/` you can check if you want.

# Steps to run this app locally with mysql


1. install redis (`https://redis.io/`)
2. install mysql
3. create database with named `dummy` in mongodb
4. `mysqldump -u username -p databasename tableName > user.sql` to import mysql
5. install requiremets using `pip install -r requirements.txt` (You can use virtualenv also as i am using)
6. run `python manage.py migrate`
7. run `python manage.py` in current directory
8. in browser run `http://127.0.0.1:8000/mongo/users/` (you can pass `?no_cache=yes` parameter with url if you don't want cached data. I explained about this inside code )


As django support ORM query we don't have to change our code doesn't matter whatever database we use.
I have added comments properly for each use cases and both db connection and how to use it for the codes.

# app structure

1. In django `settings.py` i imported db module (where all db and redis connection exist) while is inside setting folder
2. i have create one app named  `api` all api and redis logic is also inside

Please check the code inside as i added properly comment for all use cases.
