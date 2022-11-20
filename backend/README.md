# Project SOR Backend API


A modern (as of 2022) Flask API back end.

## Deploy on your Computer

### Setup

Follow these steps if you want to run this application on your computer, either
in a Docker container or as a standalone Python application.

```bash
git clone https://github.com/Nikitenko12/SOR
cd backend
cp .env.example .env
```

Open the new `.env` file and enter values for the configuration variables.

### Run with Docker

To start:

```bash
docker-compose up -d
```

The application runs on port 5000 on your 

To stop the application:

```bash
docker-compose down
```

### Run locally

Set up a Python 3 virtualenv and install the dependencies on it:

```bash
python3.10 -m venv env310
source venv/bin/activate
pip install -r dev-requirements.txt
```

Create the database and populate it with some randomly generated data:

Run the application with the Flask development web server:

```bash
flask run
```

The application runs on `localhost:5000`.

## Troubleshooting

On macOS Monterey and newer, Apple decided to use port 5000 for its AirPlay
service, which means that the Project SOR API server will not be able to run on
this port. There are two possible ways to solve this problem:

1. Disable the AirPlay Receiver service. To do this, open the System
Preferences, go to "Sharing" and uncheck "AirPlay Receiver".
2. Move Project SOR API to another port:
    - If you are running Project SOR API with Docker, add a
    `PROJECT_SOR_API_PORT=4000` line to your *.env* file. Change the 4000 to your
    desired port number.
    - If you are running Project SOR API with Python, start the server with the
    command `flask run --port=4000`.
