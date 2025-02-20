from enum import Enum

from ...public.function import getToolDir


class TranslatorIcon(Enum):

    BaiDu = "BaiDu"
    YouDao = "YouDao"

    Local = "Local"

    def path(self):
        return f"{getToolDir('translator')}/widgets/icons/Icon{self.value}.png"
