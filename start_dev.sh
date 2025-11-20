#!/bin/bash
source venv/bin/activate
python ChatApplication/manage.py migrate
redis-server --daemonize yes
cd ChatApplication && daphne -b 0.0.0.0 -p 8000 ChatApplication.asgi:application
