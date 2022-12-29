
# description
Actor system in pyton and django as frontend
at this moment it just provision and stop aws cloud instances.


Start database
```
docker-compose -f ./docker/dev/docker-compose.dev.yml up
```

migratie database

```
source venv/bin/activate
cd orc

```
star server
```
python manage.py runserver
```
