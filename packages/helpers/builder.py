
import os
from typing import Dict
from .logging_helpers import setup_logger
from .config_helpers import PackageConfig
from .os_helpers import set_directory
from pprint import pprint

logger = setup_logger(__name__)

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

    for k, v in package_config.build_args.items():
        build_args.append(k)
        build_args.append(v)

    cmd = [
        "python",
        package_config.build_script,
        "--inst", install_dir,
        package_config.build_options,
        *build_args,
        build_dir
    ]
    pprint(cmd)
    logger.info(f"Build cmd: {' '.join(cmd)}")

    with set_directory(source_dir):
        subprocess.run(cmd)