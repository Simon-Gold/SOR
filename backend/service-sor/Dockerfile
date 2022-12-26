# pull official base image
FROM python:3.10.8-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
COPY ./dev-requirements.txt /usr/src/app/dev-requirements.txt
RUN pip install -r dev-requirements.txt

# copy project
COPY . /usr/src/app/

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5001"]
