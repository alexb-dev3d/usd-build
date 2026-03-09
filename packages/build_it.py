import os, sys
import git
import logging
from json_helper import read_json

DOWNLOAD_DIR=os.environ.get("DOWNLOAD_DIR","dependencies")
BUILD_DIR=os.environ.get("BUILD_DIR","build")

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def pull_repo(repo_url: str):
    logger.info(f"Pulling repository: {repo_url}")
    



if __name__=="__main__":
    config_file = sys.argv[1]
    config_data = read_json(config_file)
    logger.info(f"Starting Usd Build for version {config_data['usd_version']}")
    pull_repo(config_data["usd_url"])