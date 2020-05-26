## What and why?

This is an example web application with MongoDB backend, powered by FastAPI.
Created as a test task for Avito internship program.

## Quickstart

With `docker-compose`
```shell
$ git clone https://github.com/tkrouty/avito-trainee-task.git
$ cd avito-trainee-task
$ docker-compose up -d
```

## Running tests

```shell
$ docker exec -it fastapi-container ./run_tests.sh
```

## Methods

#### POST /generate

Request body:
```
{
  "content" : string,
  "passphrase": string
  "delete_after_minutes": int/float -- optional
}
 ```

 #### GET /secrets/{secret_key}?passphrase={passphrase}
