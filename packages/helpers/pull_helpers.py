import os
import requests
import zipfile
import shutil
from typing import Dict
from git import Repo

from .config_helpers import PackageConfig
from .logging_helpers import setup_logger


logger = setup_logger(__name__)

def pull_repo(repo_url: str, repo_name, version_tag, download_dir: str):
    logger.info(f"Pulling repository: {repo_url}")
    dep_dir = os.path.join(os.path.abspath(os.curdir),download_dir)
    os.makedirs(dep_dir,exist_ok=True)
    repo_dir = os.path.join(dep_dir,repo_name)
    repository = Repo.clone_from(repo_url,repo_dir)
    logger.info(f"Checking out {version_tag}")
    repository.checkout(version_tag)

def pull_zip(zip_url: str, out_path: str, download_dir: str, force_pull: bool = False, force_unzip: bool = False) -> bool:
    try:
        logger.info(f"Pulling repository:\n    - {zip_url}\n    - {download_dir}")
        out_dir = os.path.join(download_dir,out_path)
        zip_name = out_dir+".zip"

        pull = True
        if os.path.exists(zip_name):
            if not force_pull:
                logger.warning("Archive file already exists, keeping it")
                pull = False

        if pull:
            os.makedirs(download_dir,exist_ok=True)
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
            zip_ref.extractall(download_dir)


    except Exception as e:
        logger.exception(f"Ooups: {e}")
        return False
    return True

def pull_package(package_config: PackageConfig, pull_dir: os.PathLike) -> bool:
    package_name = package_config.name
    logger.info(f"Pulling package: {package_name}")
    try:
        version_tag = package_config.version_tag
        # pkg_name hold the alternate name if any

        logger.info(f"Creating pull directory {pull_dir}")
        os.makedirs(pull_dir, exist_ok=True)
        _pull_dir = os.path.abspath(os.path.join(pull_dir,package_name))

        url = package_config.url
        
        if url.endswith(".git"):
            return pull_repo(url, package_name, version_tag, _pull_dir)
        
        out_path = f"{package_name}-{version_tag}"

        return pull_zip(url, out_path, pull_dir, force_pull = False, force_unzip = False)
    except Exception as e:
        logger.exception(f"Ooups: {e}")
        return False