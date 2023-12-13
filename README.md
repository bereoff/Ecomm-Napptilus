# Napptilus Ecomm Test

Below is the basic architecture, where the focus of this project was on the backend and the preparation of interactions with the frontend and external APIs.

<p align="center">
  <img src="https://github.com/bereoff/Ecomm-Napptilus/blob/main/project_images/Napptilus.png" />
</p>

---

The following steps will be presented for the local project usage.

> ## Prerequisites:
- Docker
- Docker-Compose
- API_KEY from Sendgrid, in order to achieve the email send routine well execution

First, you need to identify the location where the project repository will be cloned.

Once the location is defined, run the following command to clone it:
```
$ git clone git@github.com:bereoff/Ecomm-Napptilus.git
```

As the next step, you need to be in the project's root directory, where the run.sh file is located, and run the command:

<p align="center">
  <img src="https://github.com/bereoff/Ecomm-Napptilus/blob/main/project_images/project-root.png" />
</p>

```
$ ./run.sh
```

This command will ensure that all necessary container images are downloaded to your computer and will start three services:
- Django
- Postgres
- Cron

It will also install Python dependencies and perform other required routines for the process.

During the process, database migrations and loading of 10 products will be applied.

---

Three commands have been created to assist in debugging and testing in a local and low-complexity context.

> ## Command to clean the database
```
$ docker-compose exec django django-admin clean_db
```

> ## Command for data loading
```
$ docker-compose exec django django-admin custom_load_fixture
```

> ## Command to trigger the inventory product report
```
$ docker-compose exec django django-admin inventory_trigger
```
