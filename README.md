# personel_tracking


docker exec -it postgres_db psql -U postgres -d personel_tracking -c "\l"
docker exec -it django_core python manage.py migrate