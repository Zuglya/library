Файлы с заполненными базами данных находятся в папке DB:
Library и Library_Full делал из Postgres`а с помощью pg_dump. Отличаются настройками.
db.json и db.xml делал через терминал Django c помощью комманд python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.json и
python manage.py dumpdata --exclude auth.permission --exclude contenttypes > db.xml соответственно