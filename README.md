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
# copy files from an image.Exp; cp <image-id>:<source-PATH> <target-PATH>
docker container cp 3dab08807764:/usr/src/app ./tmp
```

## Run Backend TESTS
```
pytest -s --disable-warnings
```

## Heroku
- To use heroku cli on macos m series CPU in terminal:
```
arch -x86_64 zsh
```
## Mongo Engine Remove a Field from models.py
1. YourModel.objects.update(unset__field_name_to_delete=True)
2. remove field from class YourModel




