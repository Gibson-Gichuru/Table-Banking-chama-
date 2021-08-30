web: gunicorn manage:app
worker: rq worker -u $REDIS_URL chama-tasks