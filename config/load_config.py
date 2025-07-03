import logging
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)

env_variables = {
    "DATABASE_URL": str,
    "DATABASE_LOG_URL": str,
    "PROJECT_PHOTO_LIMIT_ROWS": int,
    "INTEGRATION_TYPE_ID": int,
    "DATABASE_LOG_FLAG": int,
    "INFO_LOG": int,
    "ERROR_MESSAGE": str
}

load_dotenv(override=True)

for key, convert in env_variables.items():
    try:
        env_variables[key] = convert(os.getenv(key))
    except Exception as error:
        logger.error(f"Error while reading env variables: {error}")

DATABASE_URL = env_variables["DATABASE_URL"]
DATABASE_LOG_URL = env_variables["DATABASE_LOG_URL"]
PROJECT_PHOTO_LIMIT_ROWS = env_variables["PROJECT_PHOTO_LIMIT_ROWS"] or 25
INTEGRATION_TYPE_ID = env_variables["INTEGRATION_TYPE_ID"]
DATABASE_LOG_FLAG = env_variables["DATABASE_LOG_FLAG"] or 0
INFO_LOG = env_variables["INFO_LOG"] or 0
ERROR_MESSAGE = env_variables["ERROR_MESSAGE"] or "Oooppppsssss...unexpected error occured! Please, examine program logs for more details"
