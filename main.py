import os
import sys
import subprocess
import pymongo
import dotenv

IMAGE_NAME = "aurora-selfbot"

dotenv.load_dotenv()

if not os.environ["MONGO_URI"]:
    print("Missing MONGO_URI env variable")
    sys.exit(1)


db = pymongo.MongoClient(os.environ["MONGO_URI"])
token_collection = db.aurora.tokens


def add_token(DISCORD_TOKEN, CANVAS_TOKEN="", CANVAS_URL="", name=""):
    payload = {"discordToken": DISCORD_TOKEN, "name": name}

    if CANVAS_TOKEN:
        payload["canvasToken"] = CANVAS_TOKEN

    if CANVAS_URL:
        payload["canvasUrl"] = CANVAS_URL

    token_collection.insert_one(payload)


def kill_containers():
    print("Killing containers...")

    os.system("docker container prune -f")
    os.system("sudo pkill -f docker")
    
    os.system(
        f'docker rm $(docker stop $(docker ps -a -q --filter ancestor={IMAGE_NAME} --format="{{{{.ID}}}}"))'
    )


def run_containers(tokens):
    kill_containers()

    for token in tokens:
        payload = [
            "docker",
            "run",
            "--name",
            token["name"].replace(" ", "_").replace("!", ""),
            "-d",
            "-e",
            f"TOKEN={token['discordToken']}",
        ]
        if "canvasToken" in token:
            payload += ["-e", f"CANVAS_TOKEN={token['canvasToken']}"]

        if "canvasUrl" in token:
            payload += ["-e", f"CANVAS_URL={token['canvasUrl']}"]

        if "loggerWebhookUrl" in token:
            payload += ["-e", f"LOGGER_WEBHOOK_URL={token['loggerWebhookUrl']}"]

        payload.append(IMAGE_NAME)

        print(f"Running {token['name']}'s selfbot")
        subprocess.run(payload)


if __name__ == "__main__":
    run_containers(token_collection.find())
