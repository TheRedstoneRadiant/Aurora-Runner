import os
import sys
import subprocess
import pymongo
import dotenv


def run_containers(tokens):
    for token in tokens:
        print(token)


def main():
    dotenv.load_dotenv()

    if not os.environ["MONGO_URI"]:
        print("Missing MONGO_URI env variable")
        sys.exit(1)

    db = pymongo.MongoClient(os.environ["MONGO_URI"])
    token_collection = db.aurora.tokens

    run_containers(token_collection.find())


if __name__ == "__main__":
    main()
