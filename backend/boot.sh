#!/bin/sh
flask db upgrade
exec gunicorn -b :5000 --access-logfile - --error-logfile - project_sor:app
