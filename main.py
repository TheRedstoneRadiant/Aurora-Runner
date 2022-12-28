import os
import sys
import subprocess
import pymongo
import dotenv


db = pymongo.MongoClient(os.environ["MONGO_URI"])
token_collection = db.aurora.tokens


def add_token(DISCORD_TOKEN, CANVAS_TOKEN=""):
    payload = {"discordToken": DISCORD_TOKEN}

    if CANVAS_TOKEN:
        payload["canvasToken"] = CANVAS_TOKEN

    token_collection.insert_one(payload)


def run_containers(tokens):
    for token in tokens:
        print(token)


def main():
    dotenv.load_dotenv()

    if not os.environ["MONGO_URI"]:
        print("Missing MONGO_URI env variable")
        sys.exit(1)

    run_containers(token_collection.find())


if __name__ == "__main__":
    main()
