
import os
import logging
from typing import Dict
from .logging_helpers import setup_logger

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