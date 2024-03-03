: ${DJANGO_SU_NAME:=admin}
: ${DJANGO_SU_EMAIL:=admin@gmail.com}
: ${DJANGO_SU_PASSWORD:=admin}

python manage.py collectstatic --no-input
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py loaddata items.json
echo "from django.contrib.auth.models import User; User.objects.create_superuser('$DJANGO_SU_NAME', '$DJANGO_SU_EMAIL', '$DJANGO_SU_PASSWORD')" | python manage.py shell
gunicorn rishat_test_task.wsgi:application --bind 0:8000