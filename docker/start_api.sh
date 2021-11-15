#!/bin/bash

source /root/.local/share/virtualenvs/synthesis-*/bin/activate

echo "<<<<<<<<<<<<<<<<<< Collect Staticfiles>>>>>>>>>>>>>>>>"
python manage.py collectstatic --noinput

sleep 10
echo "<<<<<<<< Database Setup and Migrations Starts >>>>>>>>>"
# Run database migrations
python manage.py migrate &

echo "<<<<<<< Database Setup and Migrations Complete >>>>>>>>>"
echo " "

echo " "
echo "<<<<<<<<<<<<<<<<<<<< START Celery >>>>>>>>>>>>>>>>>>>>>>"

# # start Celery worker
celery -A app worker -l info --pool=gevent --concurrency=1000 &

# start celery beat
celery -A app beat --loglevel=info &
echo " "

sleep 5
echo " "
echo "<<<<<<<<<<<<<<<<<>><<< START API >>>>>>>>>>>>>>>>>>>>>>>>>>"
# Start the API with gunicorn
gunicorn -k uvicorn.workers.UvicornH11Worker --threads=3 --bind 0.0.0.0:8000 app.asgi --reload --access-logfile '-' --workers=4
# daphne -b 0.0.0.0 -p 8000 app.asgi:application
