import json
import os
from typing import Any, Dict, Optional

# Global caching for JSON language packs
ALL_LANGUAGE_PACKS: Dict[str, Dict[str, Any]] = {"en": {}}
"""JSON语言包的全局缓存"""

DIR = os.path.dirname(os.path.abspath(__file__))


def get_language_pack(locale: str) -> Optional[Dict[str, Any]]:
    """
    获取或缓存指定语言代码的语言包。

    :param locale: 语言代码。
    :return:
    """

    pack = ALL_LANGUAGE_PACKS.get(locale)
    if not pack:
        filename = DIR + "/{}/LC_MESSAGES/messages.json".format(locale)
        try:
            with open(filename, encoding="utf8") as f:
                pack = json.load(f)
                ALL_LANGUAGE_PACKS[locale] = pack or {}
        except Exception:
            # Assuming english, client side falls back on english
            pass

    return pack
