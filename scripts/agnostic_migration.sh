python manage.py makemigrations
python manage.py showmigrations
python manage.py migrate --fake cicsa_ranking zero
find . -path "../*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "../*/migrations/*.pyc"  -delete
python manage.py makemigrations
python manage.py migrate --fake-initial
python manage.py showmigrations
