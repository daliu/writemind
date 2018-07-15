web: flask db upgrade; flask translate compile; gunicorn run:app
worker: rq worker -u $REDIS_URL writemind-tasks