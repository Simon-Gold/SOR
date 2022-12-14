# Docker
## Commands
```bash
# run flask shel with backend container name
docker exec -it sor-backend-1 flask shell
# debugging python side (stdin_open: true & tty: true => will be added services.backend in docker-compose)
docker attach <container-id>
# mongosh
docker exec -it mongodb mongosh -u developer -p developer
# see docker container ip address
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' <container-name>
```

## Run Backend TESTS
```
pytest -s --disable-warnings
```

## Heroku
- To use heroku cli on macos m series CPU in terminal:
````
arch -x86_64 zsh
```





