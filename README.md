# Django Backend

> :warning: Change Docker volumes names to specific project name in `docker-compose.yml` and `install.sh` to avoid problems when working on more than one project.

## Requirements

* Docker 19.03.0+ with a RAM limit in the container of >2000MB
* Docker Compose 1.24.0+

## Setup

Requirements for contributing to the code:

* Docker and docker compose, as is mentioned in the README.md
* [Python 3](https://www.python.org/)
* [pre-commit](https://pre-commit.com/)

Install the git hooks with:

```bash
pre-commit install
cp ./scripts/git-hook-commit-msg .git/hooks/commit-msg
```

Run the `install.sh` script:

```bash
cd /path/to/thisrepo
./install.sh
```

Start Docker containers:

```bash
docker-compose up -d
```

Create a new superuser:

```bash
docker-compose run web python manage.py createsuperuser
```

Link to <http://localhost/admin/> and log in!

### Access to the shell in a container

```bash
docker-compose run SERVICE bash
```

Service could be `database`, `web`, `redis`, etc.

### Access the Django shell with Docker

```bash
docker-compose run web python manage.py shell
```

## Testing

```bash
docker-compose run web pytest
```

## Access Mailhog in the browser

To view emails sent by the application, go to <http://localhost:8025>
