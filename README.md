Django eCommerce
============

This is a Django eCommerce API backend boilerplate powered by Postgresql, Redis, Celery and Elasticsearch (WIP).

---

## Features
- REST API
- User authentication using JWT
- Products/Categories/Orders CRUD
- Full-text search - Elasticsearch
- Thumbnail auto-generation
- Order confirmation emails
- Automatic tests - Django-pytest (products)
- pgAdmin

---

## To-do
- User registration
- Stripe integration
- Order statistics dashboard - Kibana

---

#### There are 3 user levels:
- **Client:** Can place orders
- **Manager:** Access to Products/Categories CRUD
- **Administrator:** WIP

**Demo/dev environment credentials:**
- manager:manager123
- client:client123

---

## Running using Docker 
Clone this repo. Copy/rename .env.example to .env and backend/.env.example to backend/.env, and modify them accordingly.  Run command below to start backend.
```
HOST_UID=$(id -u) HOST_GID=$(id -g) docker compose  -f docker-compose.yml up
```

---

## Running using Docker - debug mode
Clone this repo. Copy/rename .env.example to .env and backend/.env.example to backend/.env, and modify them accordingly ('ENV = \'dev'' in backend/.env).  Run command below to start in debug mode.
```
HOST_UID=$(id -u) HOST_GID=$(id -g) docker compose  -f docker-compose.yml -f docker-compose.debug.yml up
```

---

## Running tests
Start backend in debug mode. Run command below to initialize tests.
```
docker compose run --rm backend python manage.py test
```

---

## REST API Documentation
Swagger API documentation is available at:

`{SEVER_ADDRESS}/api/schema/swagger-ui/`

---

## Live demo
Live demo backend available at:

https://ecommerce-demo.hamsterburrow.pl/api/schema/swagger-ui/

---

## License
>You can check out the full license [here](https://github.com/vulkri/ecommerce/blob/master/LICENSE)

This project is licensed under the terms of the **MIT** license.
