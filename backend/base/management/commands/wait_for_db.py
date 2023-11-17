import time

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError
from psycopg2 import OperationalError as PGOperationalError

# Race condition fix based in
# https://deployeveryday.com/2016/09/12/race-condition-docker-compose.html


class Command(BaseCommand):
    help = "Wait until the database is ready for handling connections."

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            "-t",
            "--timeout",
            dest="timeout",
            type=int,
            default=1,
            help="Polling timeout in seconds",
        )

    def handle(self, *args, **options):
        while True:
            try:
                connection.connect()
            except (OperationalError, PGOperationalError):
                self.stdout.write("Error connecting to the Database. Waiting...")
                time.sleep(options["timeout"])
            else:
                self.stdout.write("Database is ready for connections.")
                break
