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
    
    