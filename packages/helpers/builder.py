
import os
from typing import List
import subprocess
from .logging_helpers import setup_logger
from .config_helpers import PackageConfig
from .os_helpers import set_directory
from pprint import pprint

logger = setup_logger(__name__)

def parse_build_args(param) -> List:
    
    if isinstance(param, (str,int,float)):
        return [str(param)]
    
    if isinstance(param, dict):
        build_args = []
        for k, v in param.items():
            build_args.append(k)
            build_args.extend(parse_build_args(v))
        return build_args

    if isinstance(param,list):
        return param

    raise Exception(f"Unsupported type for build arg: {type(param)}")

def run_build_script(
        package_config: PackageConfig,
        source_dir : os.PathLike,
        build_dir : os.PathLike,
        install_dir: os.PathLike) -> None:

    logger.info(f"Starting build script\n    - source:  {source_dir}\n    - build:   {build_dir}\n    - install: {install_dir}")
    install_dir = os.path.abspath(install_dir)

    os.makedirs(install_dir, exist_ok=True)
    os.makedirs(build_dir, exist_ok=True)

    build_args = []

    for param in package_config.build_args:
        build_args.extend(parse_build_args(param))

    cmd = [
        "python",
        package_config.build_script,
        *build_args
    ]
    pprint(cmd)
    logger.info(f"Build cmd: {' '.join(cmd)}")

    with set_directory(source_dir):
        subprocess.run(cmd)