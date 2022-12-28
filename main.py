import os
import sys
import subprocess
import mongodb
import dotenv

dotenv.load_dotenv()

if not os.environ["MONGO_URI"]:
    print("Missing MONGO_URI env variable")
    sys.exit(1)
