import os
from typing import overload


@overload
def getToolDir(toolName: str) -> str: ...

@overload
def getToolDir() -> str: ...


def getToolDir(toolName: str=None) -> str:
    if not toolName:
        return os.getcwd() + "/tool/"
    return os.getcwd() + "/tool/" + toolName + "/"
