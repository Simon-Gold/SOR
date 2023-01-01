#!/bin/sh

if [ "$DATABASE" = "mongodb" ]
then
    echo "Waiting for mongodb..."

    while ! nc -z $MONGODB_HOST $MONGODB_PORT; do
      sleep 0.1
    done

    echo "mongodbQL started"
fi

exec "$@"