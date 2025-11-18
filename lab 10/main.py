import os
import yaml

def run_app():
    secret_env = os.getenv("API_KEY")
    print("ENV secret:", secret_env)

    with open("config.yaml") as f:
        data = yaml.safe_load(f)
        print("Config file secret:", data["db_password"])

if __name__ == "__main__":
    run_app()
