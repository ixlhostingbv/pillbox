# pillbox
Our swiss-knife api-based inventory database


# Docker
docker build -t pillbox-turret .
docker run -d --name mongo -d mongo 
docker run -d --name api --link mongo:mongo pillbox-turret
docker run -d --name nginx --link -p8080:8080 api nginx

# Docker compose

docker-compose rm -f
docker-compose build --pull --no-cache
docker-compose up -d
# Run some tests
docker-compose stop -t 1

enter running container

docker exec -it <container-id> bash
