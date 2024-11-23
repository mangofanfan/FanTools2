import hashlib
from dataclasses import dataclass
from typing import Union


@dataclass
class HashData:
    sha1: str = None
    sha256: str = None
    sha384: str = None
    sha512: str = None
    md5: str = None

    def update(self, mode: str, value: str) -> None:
        if mode == "sha1":
            self.sha1 = value
        elif mode == "sha256":
            self.sha256 = value
        elif mode == "sha384":
            self.sha384 = value
        elif mode == "sha512":
            self.sha512 = value
        elif mode == "md5":
            self.md5 = value
        else:
            raise ValueError(f"Invalid mode {mode}.")

        return None


def cal_file_hash(filePath: str) -> HashData:
    data = HashData()
    with open(filePath, mode="rb") as f:
        for mode in ["sha1", "sha256", "sha384", "sha512", "md5"]:
            hc = HashCore(mode)
            hc.update(f.read())
            data.update(mode, hc.get())
    return data


class HashCore:
    def __init__(self, hashMode: str):
        """
        创建哈希值运算核心。
        :param hashMode: str, should be 'md5', 'sha1', 'sha256', 'sha384', 'sha512'.
        """
        if hashMode not in ['md5', 'sha1', 'sha256', 'sha384', 'sha512']:
            raise NameError(f"{hashMode} is not supported.")

        self.hashMode = hashMode
        if hashMode == 'md5':
            self.core = hashlib.md5()
        elif hashMode == 'sha1':
            self.core = hashlib.sha1()
        elif hashMode == 'sha256':
            self.core = hashlib.sha256()
        elif hashMode == 'sha384':
            self.core = hashlib.sha384()
        else:
            self.core = hashlib.sha512()

    def update(self, data: Union[str, bytes]):
        """
        更新数据。
        :param data: str or bytes
        :return: None
        """
        self.core.update(data)
        return None

    def get(self) -> str:
        """
        获取当前计算得出的哈希值。
        :return: str
        """
        return self.core.hexdigest()

