#!/bin/bash

# # Read the port from the environment variable, default to 5000 if not set
# PORT="${PORT:-5000}"

# # Start the Gunicorn server with the specified port
# gunicorn --bind 0.0.0.0:"$PORT" manage:create_app

python3 manage.py