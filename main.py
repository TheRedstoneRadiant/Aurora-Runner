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


def add_token(DISCORD_TOKEN, CANVAS_TOKEN="", name=""):
    payload = {"discordToken": DISCORD_TOKEN, "name": name}

    if CANVAS_TOKEN:
        payload["canvasToken"] = CANVAS_TOKEN

    token_collection.insert_one(payload)


def kill_containers():
    print("Killing containers...")
    
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
            token["name"],
            "-d",
            "-e",
            f"TOKEN={token['discordToken']}",
        ]
        if "canvasToken" in token:
            payload += ["-e", f"VLC_TOKEN={token['canvasToken']}"]

        payload.append(IMAGE_NAME)

        print(f"Running {token['name']}'s selfbot")
        subprocess.run(payload)


if __name__ == "__main__":
    run_containers(token_collection.find())
