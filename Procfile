web: gunicorn footgasm.wsgi --log-file - --log-level debug
worker: celery -A footgasm worker --loglevel=INFO  
beat: celery -A footgasm beat 