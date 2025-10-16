import undetected_chromedriver as uc  # pyright: ignore[reportMissingImports]
from selenium.webdriver.common.proxy import Proxy, ProxyType
from fake_useragent import UserAgent  # pyright: ignore[reportMissingImports]
from typing import Optional, Tuple


def build_chrome(proxy: Optional[str] = None, user_agent: Optional[str] = None, headless: bool = False) -> Tuple[uc.Chrome, str]:
    ua = user_agent or UserAgent().random

    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-extensions")
    options.add_argument("--start-maximized")
    options.add_argument(f"--user-agent={ua}")
    if headless:
        options.add_argument("--headless=new")

    if proxy:
        options.add_argument(f"--proxy-server={proxy}")

    driver = uc.Chrome(options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver, ua