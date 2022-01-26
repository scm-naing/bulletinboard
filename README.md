# Bulletinboard(Django)

## Create virtual environment

`python -m venv .venv`

## Activate virtual environment

`.venv\Scripts\activate`

## Install dependencies

`python -m pip install -r requirements.txt`

## Create MySQL database

create mysql database name with `locallibrary`

name = bulletinboard

port = 3306

host = localhost

username = root

password = root

*** if your database config not satify with above, you can fix mysql database setting in db.cnf file. ***

## Migrate database

`python manage.py makemigrations`

`python manage.py migrate`

## Create admin

`python manage.py createsuperuser`

*** Add email and password. ***

## Run app

`py manage.py runserver`

### Admin pannel

[/admin/](http://localhost:8000/admin/)

### Bulletinboard app

[/posts/](http://localhost:8000/)

## Testing

`py manage.py test`

## Testing with coverage

`coverage run --source='.' manage.py test`

`coverage report`
