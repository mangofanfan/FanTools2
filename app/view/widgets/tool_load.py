import json
import os
from dataclasses import dataclass
from typing import Generator

from app.common.function import basicFunc


@dataclass
class Tool:
    name: str
    module: str
    icon: str
    tip: str
    ver: str
    author: str
    launchMode: int

tools_dir = basicFunc.getHerePath() + "/tool"


def load_all_tools() -> Generator[Tool, None, None]:
    with os.scandir(tools_dir) as entries:
        for o in entries:
            if o.is_dir():
                try:
                    data: dict = json.loads(basicFunc.readFile(f"{tools_dir}/{o.name}/tool.json", realPath=True),)
                except FileNotFoundError:
                    continue
                else:
                    yield Tool(name=data["name"], module=data["module"],
                               icon=data["icon"], tip=data["tip"],
                               ver=data["ver"], author=data["author"],
                               launchMode=data["launchMode"])
