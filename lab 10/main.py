import os
import yaml
import requests

def run_app():
    secret_env = os.getenv("API_KEY")
    print("ENV secret:", secret_env)

    with open("config.yaml") as f:
        data = yaml.safe_load(f)
        print("Config file secret:", data["db_password"])

    VAULT_ADDR = "http://127.0.0.1:8200"
    VAULT_TOKEN = os.getenv("VAULT_TOKEN")

    url = f"{VAULT_ADDR}/v1/secret/data/app"
    headers = {"X-Vault-Token": VAULT_TOKEN}

    resp = requests.get(url, headers=headers).json()
    vault_pass = resp["data"]["data"]["password"]

    print("Vault secret:", vault_pass)

if __name__ == "__main__":
    run_app()
