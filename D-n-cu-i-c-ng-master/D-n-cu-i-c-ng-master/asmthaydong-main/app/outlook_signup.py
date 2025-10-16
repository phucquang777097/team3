import random
import string
import time
from typing import Optional, Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .browser import build_chrome
from .config import OUTLOOK_DOMAIN


def random_name() -> Tuple[str, str]:
    first_names = ["John", "Anna", "Chris", "Linh", "Huy", "Minh", "Trang"]
    last_names = ["Smith", "Nguyen", "Tran", "Pham", "Le", "Hoang", "Vo"]
    return random.choice(first_names), random.choice(last_names)


def random_username() -> str:
    letters = string.ascii_lowercase
    return "".join(random.choices(letters, k=8)) + str(random.randint(100, 999))


def random_password() -> str:
    chars = string.ascii_letters + string.digits + "!@#$%"
    pwd = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice("!@#$%"),
    ]
    pwd += random.choices(chars, k=8)
    random.shuffle(pwd)
    return "".join(pwd)


def create_outlook_account(proxy: Optional[str] = None, headless: bool = False) -> Tuple[Optional[str], Optional[str]]:
    driver, ua = build_chrome(proxy=proxy, headless=headless)
    wait = WebDriverWait(driver, 20)
    try:
        driver.get("https://signup.live.com/")
        time.sleep(2)

        username = random_username()
        email = f"{username}@{OUTLOOK_DOMAIN}"
        password = random_password()
        
        # Fill email field directly
        email_field = wait.until(EC.presence_of_element_located((By.NAME, "MemberName")))
        email_field.clear()
        email_field.send_keys(email)

        # Next (Đã cập nhật bộ chọn)
        next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='primaryButton'][type='submit']")))
        next_btn.click()
        time.sleep(2.5) # Tăng nhẹ thời gian chờ để chắc chắn chuyển trang

        # Password
        pwd_field = wait.until(EC.presence_of_element_located((By.ID, "PasswordInput")))
        pwd_field.clear()
        pwd_field.send_keys(password)
        # Cập nhật bộ chọn
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='primaryButton'][type='submit']"))).click()
        time.sleep(2.5) # Tăng nhẹ thời gian chờ

        # Names
        first, last = random_name()
        wait.until(EC.presence_of_element_located((By.NAME, "FirstName"))).send_keys(first)
        wait.until(EC.presence_of_element_located((By.NAME, "LastName"))).send_keys(last)
        wait.until(EC.element_to_be_clickable((By.ID, "iSignupAction"))).click()

        # Birth date — simplified (you can enhance with Select)
        time.sleep(1.5)
        try:
            wait.until(EC.presence_of_element_located((By.NAME, "Country"))).send_keys("Vietnam")
        except Exception:
            pass
        try:
            wait.until(EC.presence_of_element_located((By.NAME, "BirthDay"))).send_keys("15")
            wait.until(EC.presence_of_element_located((By.NAME, "BirthMonth"))).send_keys("5")
            wait.until(EC.presence_of_element_located((By.NAME, "BirthYear"))).send_keys("1996")
        except Exception:
            pass
        wait.until(EC.element_to_be_clickable((By.ID, "iSignupAction"))).click()

        # Captcha step - manual
        print("[Manual] Solve captcha in the opened browser, then press Enter here...")
        input()

        # Post-captcha confirm
        time.sleep(2)
        return email, password

    except Exception as e:
        print("Signup error:", e)
        return None, None
    finally:
        try:
            time.sleep(3)
            driver.quit()
        except Exception:
            pass




