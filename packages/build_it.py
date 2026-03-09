import os, sys
from git import Repo
#import logging
import requests
import zipfile
import shutil
from json_helper import read_json
from logging_helper import setup_logger

DOWNLOAD_DIR=os.environ.get("DOWNLOAD_DIR","dependencies")
BUILD_DIR=os.environ.get("BUILD_DIR","build")

# logging.basicConfig(level=logging.INFO)
#logger = logging.getLogger(__name__)
logger = setup_logger(__name__)

def pull_repo(repo_url: str, repo_name, version_tag):
    logger.info(f"Pulling repository: {repo_url}")
    dep_dir = os.path.join(os.path.abspath(os.curdir),DOWNLOAD_DIR)
    os.makedirs(dep_dir,exist_ok=True)
    repo_dir = os.path.join(dep_dir,repo_name)
    repository = Repo.clone_from(repo_url,repo_dir)
    logger.info(f"Checking out {version_tag}")
    repository.checkout(version_tag)

def pull_zip(zip_url: str, out_path: str, force_pull: bool = False, force_unzip: bool = False) -> bool:
    try:
        logger.info(f"Pulling repository: {zip_url}")
        dep_dir = os.path.join(os.path.abspath(os.curdir),DOWNLOAD_DIR)
        out_dir = os.path.join(dep_dir,out_path)
        zip_name = out_dir+".zip"

        pull = True
        if os.path.exists(zip_name):
            if not force_pull:
                logger.warning("Archive file already exists, keeping it")
                pull = False

        if pull:
            os.makedirs(dep_dir,exist_ok=True)
            with open(zip_name,"wb") as zip_file:
                content = requests.get(zip_url, stream=True).content
                zip_file.write(content)

        if os.path.exists(out_dir):
            # you do not always to force the unzip if ever you have made tweaks to the original
            if not force_unzip:
                logger.warning(f"Destination folder {out_dir} exists and force unzip is False, keeping dest folder as is")
                return True
            logger.warning("Forcing removing of unzipped folder")
            shutil.rmtree(out_dir)

        logger.info("Unzipping file")
        with zipfile.ZipFile(zip_name, 'r') as zip_ref:
            zip_ref.extractall(dep_dir)


    except Exception as e:
        logger.exception(f"Ooups: {e}")
        return False
    return True

if __name__=="__main__":
    print(sys.argv[0], os.path.abspath(os.curdir))
    config_file = sys.argv[1]
    config_data = read_json(config_file)
    logger.info(f"Starting Usd Build for version {config_data['usd_version_tag']}")
    version_tag = config_data["usd_version_tag"]
    # pull_repo(config_data["usd_url"], f"OpenUsd{version_tag}", version_tag)
    pull_zip(config_data["usd_url"], f"OpenUsd-{version_tag}", force_unzip = True)