import json

import boto3


class SecretManager:
    def __init__(self, secret_name):
        self.secret_name = secret_name
        self.client = boto3.client("secretsmanager", region_name="us-east-1")
        self.secrets_cache = {}

    def get_secret(self, key):
        if key in self.secrets_cache:
            return self.secrets_cache[key]

        response = self.client.get_secret_value(SecretId=self.secret_name)
        secret_value = response["SecretString"]
        secrets = json.loads(secret_value)

        if key in secrets:
            self.secrets_cache[key] = secrets[key]
            return secrets[key]
        else:
            msg = f"Key '{key}' not found in secrets."
            raise KeyError(msg)
