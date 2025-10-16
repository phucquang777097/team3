import time
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .browser import build_chrome


def outlook_warmup(email: str, password: str, proxy: Optional[str] = None, headless: bool = False) -> bool:
    driver, ua = build_chrome(proxy=proxy, headless=headless)
    wait = WebDriverWait(driver, 20)
    try:
        driver.get("https://outlook.live.com/mail/")
        time.sleep(2)

        # Login
        wait.until(EC.presence_of_element_located((By.NAME, "loginfmt"))).send_keys(email)
        wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
        wait.until(EC.presence_of_element_located((By.NAME, "passwd"))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.ID, "idSIButton9"))).click()
        time.sleep(3)

        # Simple actions (open inbox)
        driver.get("https://outlook.live.com/mail/0/inbox")
        time.sleep(5)
        return True
    except Exception as e:
        print("Warm-up error:", e)
        return False
    finally:
        try:
            time.sleep(2)
            driver.quit()
        except Exception:
            pass




