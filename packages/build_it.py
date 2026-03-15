import os, sys
import subprocess
from argparse import Namespace
from typing import Dict
from helpers.config_helpers import ConfigHelper
from helpers.logging_helpers import setup_logger
from helpers.os_helpers import set_directory
from helpers.pull_helpers import pull_package, pull_zip

DOWNLOAD_DIR=os.environ.get("DOWNLOAD_DIR","dependencies")
BUILD_DIR=os.environ.get("BUILD_DIR","build")

# logging.basicConfig(level=logging.INFO)
logger = setup_logger(__name__)

    
def run_build_script(out_path: str, config_data: Dict, install_dir: os.PathLike) -> None:

    logger.info("Starting build script")
    usd_root = os.path.join(os.path.abspath(os.curdir),DOWNLOAD_DIR,out_path)
    build_dir = os.path.join(os.path.abspath(os.curdir),BUILD_DIR,out_path)
    build_script_path = os.path.join("build_scripts","build_usd.py")
    install_dir = os.path.abspath(install_dir)

    _build_args = config_data.get("build_args",{})
    build_args = []

    for k, v in _build_args.items():
        build_args.append(k)
        build_args.append(v)

    cmd = [
        "python",
        build_script_path,
        "--inst", install_dir,
        *config_data.get("build_options",[]),
        *build_args,
        build_dir
    ]
    logger.info(f"Build cmd: {' '.join(cmd)}")

    with set_directory(usd_root):
        subprocess.run(cmd)

def parse_arguments() ->Namespace:
    import argparse
    parser = argparse.ArgumentParser(description="Build script for packages and its dependencies")
    parser.add_argument("--config", help="Path to the config file", required = True)
    parser.add_argument("--pull_dir", help="Path to the pull directory", default = r"..\3rd_parties\pull")
    parser.add_argument("--install_dir", help="Path to the install directory", default = r"..\3rd_parties")
    return parser.parse_args(sys.argv[1:])


def pull_package(config, package_name, args):
    logger.info(f"Pulling package: {package_name}")
    print("args", args)
    pull_dir = args.pull_dir
    if not pull_package(config, package_name, pull_dir):
        logger.error("Failed pulling dependencies")
        exit(0)


    version_tag = config_data.package_version_tag(package_name)
    logger.info(f"Starting Usd Build for version {version_tag}")
    logger.info(f"Will install in: {install_dir}")
    # pull_repo(config_data["usd_url"], f"OpenUsd{version_tag}", version_tag)
    out_dir_name = f"OpenUsd-{version_tag}"
    if not pull_zip(config_data["usd_url"], out_dir_name, force_unzip = False):
        logger.error("Failed pulling dependencies")
        exit(0)

    install_dir = os.path.join(install_dir, out_dir_name)
    run_build_script(out_dir_name, config_data, install_dir)

if __name__=="__main__":
    args = parse_arguments()
    
    config = ConfigHelper(args.config)

    logger.info(f"Building packages {config.packages()}")
    for package in config.packages():
        package_config = config.package_class(package)
        print( package_config)
        pull_package(config, package, args)

