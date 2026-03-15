import json
import re
from os import PathLike
from typing import Dict

class JSONWithCommentsDecoder(json.JSONDecoder):
    def __init__(self, **kwgs):
        super().__init__(**kwgs)

    def decode(self, s: str):
        regex = r"""("(?:\\"|[^"])*?")|(\/\*(?:.|\s)*?\*\/|\/\/.*)"""
        s = re.sub(regex, r"\1", s)  # , flags = re.X | re.M)
        return super().decode(s)
    

def read_json(file_path: PathLike) -> Dict:
    with open(file_path) as f:
        return json.loads(f.read(), cls=JSONWithCommentsDecoder)
    
    

class ConfigHelper:
    config_data: Dict

    def __init__(self, config_path: PathLike):
        self.config_data = read_json(config_path)
    
    def __config(self) -> Dict:
        return self.config_data
    
    def packages(self) -> Dict:
        return self.config_data.keys()
    
    def package_url(self, package_name: str) -> str:
        return self.config_data[package_name]["url"]
    
    def package_version_tag(self, package_name: str) -> str:
        return self.config_data[package_name]["version_tag"]

    def package_name(self, package_name: str) -> str:
        """
        return the name if specified in the packagge config, otherwise return the package name as is
        """
        return self.config_data[package_name].get("name", package_name)