# cohost api
This repo contains the backend API for cohost application.  It is a python flask application with a PostgreSQL database.


## Development

Start Postgres DB in docker
```
docker-compose up -d
```

Initialize database models
```
make resetdb
```

Start application in development mode
```
make run
```
