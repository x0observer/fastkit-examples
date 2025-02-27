import os
from dotenv import load_dotenv


LOCAL_VARIABLES_FILE = ".env"
load_dotenv(LOCAL_VARIABLES_FILE, override=True)


DATABASE_USER = os.environ["DATABASE_USER"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]
DATABASE_NAME = os.environ["DATABASE_NAME"]
DATABASE_URI = os.environ["DATABASE_URI"]
DATABASE_PORT = os.environ["DATABASE_PORT"]


# AUTH_SECRET_KEY = os.environ["AUTH_SECRET_KEY"]
# AUTH_ALGORITHM = os.environ["AUTH_ALGORITHM"]
# AUTH_ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["AUTH_ACCESS_TOKEN_EXPIRE_MINUTES"]


SERVER_HOST = os.environ["SERVER_HOST"]
SERVER_PORT = int(os.environ["SERVER_PORT"])
RELOAD = os.environ["RELOAD"] == "True"
TIMEOUT_KEEP_ALIVE = int(os.environ["TIMEOUT_KEEP_ALIVE"])


SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://%s:%s@%s:%s/%s" % (
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_URI,
    DATABASE_PORT,
    DATABASE_NAME,
)

settings = {"db": {"uri": SQLALCHEMY_DATABASE_URL},
            # "auth": {"secret_key": AUTH_SECRET_KEY,
            #          "algorithm": AUTH_ALGORITHM,
            #          "access_token_expire_minutes": AUTH_ACCESS_TOKEN_EXPIRE_MINUTES},
            }
print(f".env is uploaded successfully: {settings}")
