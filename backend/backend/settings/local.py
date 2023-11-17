from pathlib import Path  # python3 only

from dotenv import load_dotenv

from backend.settings.base import *  # NOQA

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path, verbose=True)

DEBUG = True
# On certain platforms (Windows 10), you might need to edit ALLOWED_HOSTS
# and add your Docker host name or IP address to the list.
# For allowing all circunstances we set the value to all the hosts
ALLOWED_HOSTS = ["*"]

AWS_DEFAULT_ACL = None
