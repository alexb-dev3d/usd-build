import os, sys
import subprocess
from argparse import Namespace
from typing import Dict
from helpers.config_helpers import ConfigHelper
from helpers.logging_helpers import setup_logger
from helpers.os_helpers import set_directory
import helpers.pull_helpers as p_helper

DOWNLOAD_DIR=os.environ.get("DOWNLOAD_DIR","dependencies")
BUILD_DIR=os.environ.get("BUILD_DIR","build")

# logging.basicConfig(level=logging.INFO)
logger = setup_logger(__name__)

    

def parse_arguments() ->Namespace:
    import argparse
    parser = argparse.ArgumentParser(description="Build script for packages and its dependencies")
    parser.add_argument("--config", help="Path to the config file", required = True)
    parser.add_argument("--pull_dir", help="Path to the pull directory", default = r"..\3rd_parties\pull")
    parser.add_argument("--install_dir", help="Path to the install directory", default = r"..\3rd_parties")
    return parser.parse_args(sys.argv[1:])


def pull_package(package_config, args):
    package_name = package_config.name
    logger.info(f"Pulling package: {package_config.name}")
    print("args", args)
    pull_dir = args.pull_dir
    if not p_helper.pull_package(package_config, pull_dir):
        logger.error("Failed pulling dependencies")
        exit(0)

def build_package(package_config, args):
    version_tag = package_config.version_tag

    run_build_script(out_dir_name, config_data, install_dir)

if __name__=="__main__":
    args = parse_arguments()
    
    config = ConfigHelper(args.config)

    logger.info(f"Building packages {config.packages()}")
    for package in config.packages():
        package_config = config.package_class(package)
        pull_package(package_config, args)

