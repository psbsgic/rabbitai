import json
import os
from typing import Any, Dict, Optional

# Global caching for JSON language packs
ALL_LANGUAGE_PACKS: Dict[str, Dict[str, Any]] = {"zh": {}}

DIR = os.path.dirname(os.path.abspath(__file__))


def get_language_pack(locale: str) -> Optional[Dict[str, Any]]:
    """Get/cache a language pack

    Returns the langugage pack from cache if it exists, caches otherwise

    >>> get_language_pack('fr')['Dashboards']
    "Tableaux de bords"
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
