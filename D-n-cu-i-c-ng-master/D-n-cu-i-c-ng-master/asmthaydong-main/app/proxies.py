import random
import time
import requests
from typing import Optional, List

from .config import PROXY_LIST_PATH


def load_proxies() -> List[str]:
    try:
        with open(PROXY_LIST_PATH, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f.readlines() if l.strip() and not l.startswith("#")]
        return lines
    except FileNotFoundError:
        return []


def choose_proxy() -> Optional[str]:
    proxies = load_proxies()
    if not proxies:
        return None
    return random.choice(proxies)


def verify_proxy(proxy: str, timeout: int = 12) -> bool:
    try:
        r = requests.get("https://api.ipify.org?format=json", proxies={"http": proxy, "https": proxy}, timeout=timeout)
        return r.status_code == 200
    except Exception:
        return False




