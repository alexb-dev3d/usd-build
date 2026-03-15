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
    
    
class PackageConfig:
    pass

class ConfigHelper:
    config_data: Dict

    def __init__(self, config_path: PathLike):
        self.config_data = read_json(config_path)
    
    def packages(self) -> Dict:
        return self.config_data.keys()
    
    def package_class(self, package_name: str) -> str:

        config = PackageConfig();

        for k, v in self.config_data[package_name].items():
            setattr(config, k, v)

        return config