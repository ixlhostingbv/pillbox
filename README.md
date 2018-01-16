# pillbox
Our swiss-knife api-based inventory database


# Docker
docker pull mongo:3.6
docker run --name pillbox-mongo -d mongo --auth
docker exec -it pillbox-mongo mongo admin
connecting to: admin
> db.createUser({ user: 'turretadmin', pwd: 'Tee9Xei9eiKe', roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] });

