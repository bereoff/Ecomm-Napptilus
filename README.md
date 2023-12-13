# Napptilus Ecomm Test

Below is the basic architecture, where the focus of this project was on the backend and the preparation of interactions with the frontend and external APIs.

<p align="center">
  <img src="g" />
</p>

—

The following steps will be presented for the local project usage.

> ## Prerequisites:
- Docker
- Docker-Compose

First, you need to identify the location where the project repository will be cloned.

Once the location is defined, run the following command to clone it:
```
$ git clone git@github.com:bereoff/Ecomm-Napptilus.git
```

As the next step, you need to be in the project's root directory, where the docker-compose.yml file is located, and run the command:

<p align="center">
  <img src="" />
</p>

```
$ docker-compose up --build
```

This command will ensure that all necessary container images are downloaded to your computer and will start two services:
- Django
- Postgres

It will also install Python dependencies and perform other required routines for the process.

During the process, database migrations and loading of 10 products will be applied.

---

Three commands have been created for data loading for testing in both apps, and to perform the execution, it is necessary for the services to be up and running.

> ## Command to clean the database
```
$ docker-compose exec django django-admin clean_db
```

> ## Command for data loading
```
$ docker-compose exec django django-admin custom_load_fixture
```

> ## Command to trigger the inventory product report shipment calculation
```
$ docker-compose exec django django-admin inventory_trigger
```