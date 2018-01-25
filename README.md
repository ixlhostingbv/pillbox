# pillbox
Our swiss-knife api-based inventory database


# Docker
docker build -t pillbox-turret .
docker pull mongo:3.6
docker run -d --name pillbox-mongo -d mongo 
docker run -d --name api --link pillbox-mongo:mongo pillbox-turret

