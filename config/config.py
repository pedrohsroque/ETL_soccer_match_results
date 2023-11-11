import os
from dotenv import load_dotenv

load_dotenv()

db_credentials = {
    'host': os.environ["host"],
    'database': os.environ["database"],
    'user': os.environ["user"],
    'password': os.environ["password"],
}
