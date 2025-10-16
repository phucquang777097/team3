from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
import time
import random
import string
import datetime
import os
import threading
import tkinter as tk
from tkinter import ttk

class HotmailAutoCreator:
    def __init__(self, fast: bool = False):
        self.driver = None
        self.wait = None
        self.fast = fast
    
    def setup_driver(self):
        """Cài đặt Chrome driver tự động"""
        print("🚀 Đang khởi động Chrome...")
        try:
            # Tắt log của webdriver_manager
            os.environ['WDM_LOG'] = '0'
            
            service = Service(ChromeDriverManager().install())
            
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-extensions')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--start-maximized')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            # Tối ưu tốc độ khi fast mode
            if self.fast:
                prefs = {
                    'profile.managed_default_content_settings.images': 2,
                    'profile.default_content_setting_values.notifications': 2,
                }
                options.add_experimental_option('prefs', prefs)
                options.set_capability('pageLoadStrategy', 'eager')
            
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 12 if self.fast else 15)
            
            # Ẩn automation
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            print("✅ Chrome đã sẵn sàng!")
            return True
        except Exception as e:
            print(f"❌ Lỗi khởi động Chrome: {e}")
            return False

    def generate_username(self):
        """Tạo username ngẫu nhiên"""
        adjectives = ['happy', 'smart', 'cool', 'fast', 'quick', 'sunny', 'suvatquang', 'brave', 'calm', 'proud']
        nouns = ['tiger', 'eagle', 'dragon', 'wolf', 'lion', 'fox', 'bear', 'hawk','suvatkhanh' , 'shark', 'panda']
        numbers = ''.join(random.choices(string.digits, k=4))
        
        username = f"{random.choice(adjectives)}{random.choice(nouns)}{numbers}"
        return username.lower()

    def generate_password(self):
        """Tạo password mạnh"""
        uppercase = string.ascii_uppercase
        lowercase = string.ascii_lowercase
        digits = string.digits
        symbols = "!@#$%"
        
        password = [
            random.choice(uppercase),
            random.choice(lowercase), 
            random.choice(digits),
            random.choice(symbols)
        ]
        
        all_chars = uppercase + lowercase + digits + symbols
        password += random.choices(all_chars, k=8)
        random.shuffle(password)
        return ''.join(password)

    def generate_birthdate(self):
        """Tạo ngày sinh hợp lệ (trên 18 tuổi)"""
        current_year = datetime.datetime.now().year
        year = random.randint(current_year - 50, current_year - 18)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        return day, month, year

    def random_delay(self, min_time=1, max_time=3):
        """Tạo độ trễ ngẫu nhiên giữa các action"""
        scale = 0.3 if self.fast else 1.0
        delay = random.uniform(min_time, max_time) * scale
        time.sleep(delay)

    def wait_and_click(self, by, value, description=""):
        """Chờ element và click"""
        try:
            if description:
                print(f"👉 Đang click: {description}")
            element = self.wait.until(EC.element_to_be_clickable((by, value)))
            try:
                element.click()
            except Exception:
                try:
                    # Scroll vào giữa màn hình rồi click lại
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    time.sleep(0.3)
                    element.click()
                except Exception:
                    try:
                        # Dùng ActionChains
                        ActionChains(self.driver).move_to_element(element).pause(0.1).click().perform()
                    except Exception:
                        # Fallback JS click
                        self.driver.execute_script("arguments[0].click();", element)
            self.random_delay(1, 2)
            return True
        except Exception as e:
            print(f"❌ Không thể click {description}: {e}")
            return False

    def wait_and_send_keys(self, by, value, keys, description=""):
        """Chờ element và gõ text"""
        try:
            if description:
                print(f"📝 Đang điền: {description}")
            element = self.wait.until(EC.presence_of_element_located((by, value)))
            try:
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            except Exception:
                pass
            try:
                element.clear()
            except Exception:
                pass
            # Cố gõ bình thường
            try:
                element.send_keys(keys)
            except Exception:
                pass
            # Nếu chưa có giá trị, thử ActionChains
            try:
                val = element.get_attribute("value") or ""
            except Exception:
                val = ""
            if not val:
                try:
                    ActionChains(self.driver).move_to_element(element).click().pause(0.1).send_keys(keys).perform()
                except Exception:
                    pass
            # Nếu vẫn trống, fallback JS + events
            try:
                val = element.get_attribute("value") or ""
            except Exception:
                val = ""
            if not val:
                try:
                    self.driver.execute_script(
                        "var el=arguments[0],v=arguments[1]; el.value=v; el.dispatchEvent(new Event('input',{bubbles:true})); el.dispatchEvent(new Event('change',{bubbles:true}));",
                        element,
                        keys,
                    )
                except Exception:
                    pass
            self.random_delay(1, 2)
            return True
        except Exception as e:
            print(f"❌ Không thể điền {description}: {e}")
            return False

    def is_present(self, by, value, timeout=3):
        """Kiểm tra nhanh phần tử có xuất hiện (không cần clickable)"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except Exception:
            return False

    def send_keys_any(self, candidates, keys, description=""):
        """Thử điền text theo nhiều selector cho cùng một field"""
        for by, value in candidates:
            if self.wait_and_send_keys(by, value, keys, description):
                return True
        return False

    def find_any(self, candidates, timeout=6):
        """Tìm element theo danh sách selector, trả về element đầu tiên tìm thấy"""
        last_err = None
        for by, value in candidates:
            try:
                el = WebDriverWait(self.driver, timeout).until(
                    EC.presence_of_element_located((by, value))
                )
                return el
            except Exception as e:
                last_err = e
                continue
        if last_err:
            raise last_err
        return None

    def wait_for_any(self, candidates, timeout=10):
        """Đợi cho đến khi 1 trong các selector xuất hiện, trả về True nếu thấy"""
        end = time.time() + timeout
        while time.time() < end:
            for by, value in candidates:
                try:
                    if self.driver.find_elements(by, value):
                        return True
                except Exception:
                    continue
            time.sleep(0.2)
        return False

    def select_country_and_birthdate(self):
        """Chọn khu vực (Country) và điền thông tin ngày sinh từ combobox (Tháng, Ngày) và input (Năm)"""
        try:
            print("6. Đang điền thông tin bổ sung (khu vực và ngày sinh)...")
            
            # Đợi form xuất hiện
            try:
                self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@name='Country' or @name='BirthDay' or @name='BirthMonth' or @name='BirthYear']")))
            except Exception:
                pass

            # Tạo dữ liệu ngày sinh
            day, month_num, year = self.generate_birthdate()  # Đổi tên biến month thành month_num
            month_names = ["", "January", "February", "March", "April", "May", "June", 
                           "July", "August", "September", "October", "November", "December"]
            month_name = month_names[month_num]  # Tên tháng dạng text

            # Chọn khu vực (Country)
            try:
                country_el = None
                for by, val in [
                    (By.NAME, "Country"),
                    (By.CSS_SELECTOR, "select[name='Country']"),
                ]:
                    els = self.driver.find_elements(by, val)
                    if els:
                        country_el = els[0]
                        break
                if country_el:
                    try:
                        Select(country_el).select_by_visible_text("Vietnam")
                    except Exception:
                        self.driver.execute_script(
                            "arguments[0].value='VN'; arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", country_el)
                    current_val = country_el.get_attribute('value')
                    if current_val not in ['VN', 'Vietnam', 'Viet Nam']:
                        print("[WARNING] Chọn Country có thể chưa chính xác.")
            except Exception:
                pass

            self.random_delay(0.3, 0.6)
            
            # --- Cố gắng chọn Tháng và Ngày bằng cách Click Combobox/Select/Fallback ---
            if self.driver.find_elements(By.XPATH, "//*[@role='combobox' and contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'month')]") \
               and self.driver.find_elements(By.XPATH, "//*[@role='combobox' and contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'day')]"):
                
                print("[DATE] Chọn Tháng và Ngày qua aria-combobox (Click)")
                if not self.auto_select_combobox_click_option("month"): 
                    print("[WARNING] Chọn Tháng combobox thất bại, đang điền bằng input")
                    self.wait_and_send_keys(By.NAME, "BirthMonth", str(month_num), "BirthMonth")
                if not self.auto_select_combobox_click_option("day"):
                    print("[WARNING] Chọn Ngày combobox thất bại, đang điền bằng input")
                    self.wait_and_send_keys(By.NAME, "BirthDay", str(day), "BirthDay")
            elif self.is_present(By.NAME, "BirthMonth", timeout=2) and self.is_present(By.NAME, "BirthDay", timeout=2):
                print("[DATE] Chọn Tháng và Ngày qua <select> tag (Select object/Click)")
                try:
                    Select(self.driver.find_element(By.NAME, "BirthMonth")).select_by_value(str(month_num))
                    print("[INFO] Đã chọn Month qua Select (Click)")
                except:
                    print("[WARNING] Chọn Month qua Select thất bại, dùng input")
                    self.wait_and_send_keys(By.NAME, "BirthMonth", str(month_num), "BirthMonth")
                try:
                    Select(self.driver.find_element(By.NAME, "BirthDay")).select_by_value(str(day))
                    print("[INFO] Đã chọn Day qua Select (Click)")
                except:
                    print("[WARNING] Chọn Day qua Select thất bại, dùng input")
                    self.wait_and_send_keys(By.NAME, "BirthDay", str(day), "BirthDay")
            else:
                print("[DATE] Fallback: Dùng send_keys cho Month, Day, Year")
                self.wait_and_send_keys(By.NAME, "BirthDay", str(day), "BirthDay")
                self.wait_and_send_keys(By.NAME, "BirthMonth", str(month_num), "BirthMonth")
            
            self.wait_and_send_keys(By.NAME, "BirthYear", str(year), "BirthYear")
            self.random_delay(0.5, 1)
            
            # Tự động click nút Next sau khi điền xong thông tin
            next_candidates = [
                (By.ID, "iSignupAction"),
                (By.XPATH, "//button[@data-testid='primaryButton' and contains(., 'Next')]")
            ]
            if self.click_any(next_candidates, "Next sau Birthdate"):
                self.random_delay(1, 2)
            
            print("✅ Đã điền xong thông tin bổ sung")
            return True

        except Exception as e:
            print(f"❌ Lỗi điền thông tin bổ sung: {e}")
            return False

    def dismiss_overlays_and_cookies(self):
        """Đóng popup cookie/overlay nếu có, để tránh che nút 'Tạo email mới'"""
        try:
            # Một số trang có banner cookie/consent của Microsoft
            selectors = [
                (By.ID, "accept"),
                (By.ID, "idBtn_Accept"),
                (By.ID, "acceptButton"),
                (By.XPATH, "//button[contains(., 'Accept') or contains(., 'I agree') or contains(., 'Đồng ý')]"),
            ]
            for by, value in selectors:
                try:
                    btn = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((by, value))
                    )
                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
                    time.sleep(0.2)
                    try:
                        btn.click()
                    except Exception:
                        self.driver.execute_script("arguments[0].click();", btn)
                    self.random_delay(0.5, 1)
                    break
                except Exception:
                    continue
        except Exception:
            pass

    def click_any(self, candidates, description=""):
        """Thử click theo nhiều selector cho cùng một hành động"""
        for by, value in candidates:
            if self.wait_and_click(by, value, description):
                return True
        return False

    def press_enter_on(self, candidates, description=""):
        """Thử focus và nhấn Enter trên một input/button"""
        for by, value in candidates:
            try:
                el = self.wait.until(EC.presence_of_element_located((by, value)))
                try:
                    self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
                except Exception:
                    pass
                try:
                    el.click()
                except Exception:
                    pass
                try:
                    el.send_keys(Keys.RETURN)
                    self.random_delay(1, 2)
                    return True
                except Exception:
                    continue
            except Exception:
                continue
        return False

    def submit_parent_form(self, candidates):
        """Tìm phần tử và submit form cha bằng JS"""
        for by, value in candidates:
            try:
                el = self.wait.until(EC.presence_of_element_located((by, value)))
                self.driver.execute_script(
                    "var el=arguments[0]; while(el && el.tagName!=='FORM'){el=el.parentElement;} if(el){el.submit();}",
                    el,
                )
                self.random_delay(1, 2)
                return True
            except Exception:
                continue
        return False

    def fill_password_fast_and_next(self, password):
        """Điền password cực nhanh và chuyển sang form kế tiếp (tên hoặc ngày sinh)"""
        password_candidates = [
            (By.ID, "PasswordInput"),
            (By.NAME, "passwd"),
            (By.NAME, "Password"),
            (By.CSS_SELECTOR, "input[type='password']"),
        ]

        # Tìm và focus
        el = self.find_any(password_candidates, timeout=8)
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
        except Exception:
            pass
        try:
            el.click()
        except Exception:
            pass

        # Xoá nội dung hiện có
        try:
            el.clear()
        except Exception:
            pass
        try:
            ActionChains(self.driver).move_to_element(el).click().key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL).send_keys(Keys.BACKSPACE).perform()
        except Exception:
            pass

        # Gõ thường
        try:
            el.send_keys(password)
        except Exception:
            pass

        # Nếu vẫn trống, gõ qua ActionChains
        try:
            if not (el.get_attribute('value') or ''):
                ActionChains(self.driver).move_to_element(el).click().pause(0.05).send_keys(password).perform()
        except Exception:
            pass

        # Nếu vẫn trống, set bằng JS + events
        try:
            if not (el.get_attribute('value') or ''):
                self.driver.execute_script(
                    "var e=arguments[0],v=arguments[1]; e.value=v; e.dispatchEvent(new Event('input',{bubbles:true})); e.dispatchEvent(new Event('change',{bubbles:true}));",
                    el,
                    password,
                )
        except Exception:
            pass

        # Bấm Next/Enter
        next_candidates = [
            (By.ID, "iSignupAction"),
            (By.CSS_SELECTOR, "#iSignupAction"),
            (By.XPATH, "//input[@type='submit' and (contains(@value,'Next') or contains(@value,'Tiếp'))]"),
            (By.XPATH, "//button[contains(., 'Next') or contains(., 'Tiếp')]")
        ]
        if not self.click_any(next_candidates, "Next sau Password (fast)"):
            try:
                el.send_keys(Keys.RETURN)
            except Exception:
                pass
            if not self.click_any(next_candidates, "Next sau Password (retry)"):
                self.submit_parent_form([(By.ID, "PasswordInput")])

        # Đợi màn tiếp theo (tên hoặc birth)
        if not self.wait_for_any([(By.NAME, "FirstName"), (By.NAME, "BirthDay"), (By.NAME, "BirthMonth"), (By.NAME, "BirthYear")], timeout=10):
            # click lại một lần
            self.click_any(next_candidates, "Next confirm")
            if not self.wait_for_any([(By.NAME, "FirstName"), (By.NAME, "BirthDay"), (By.NAME, "BirthMonth"), (By.NAME, "BirthYear")], timeout=8):
                raise Exception("Không thể chuyển sang màn hình tiếp theo sau Password")
        return True

    def solve_captcha_manually(self):
        """Chờ người dùng giải CAPTCHA thủ công"""
        print("\n" + "🛑" * 20)
        print("🛑 CẦN GIẢI CAPTCHA THỦ CÔNG!")
        print("👉 Vui lòng giải CAPTCHA trong trình duyệt...")
        print("👉 SAU KHI GIẢI XONG, NHẤN ENTER TRONG CONSOLE NÀY")
        print("🛑" * 20)
        
        input("⏸️ Nhấn Enter sau khi giải CAPTCHA xong...")
        return True

    def complete_verification(self):
        """Hoàn thành xác minh sau CAPTCHA"""
        try:
            print("8. Đang hoàn tất đăng ký...")
            
            # Chờ và click nút Next/Submit cuối cùng
            submit_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' or contains(@value, 'Next')]"))
            )
            submit_btn.click()
            self.random_delay(5, 8)
            
            # Kiểm tra các trang xác minh tiếp theo
            for i in range(3):
                try:
                    # Kiểm tra nếu có trang tiếp theo
                    next_btn = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' or contains(@value, 'Next')]"))
                    )
                    next_btn.click()
                    self.random_delay(3, 5)
                    print(f"✅ Đã qua bước xác minh {i+1}")
                except:
                    break
            
            # Kiểm tra kết quả cuối cùng
            time.sleep(5)
            current_url = self.driver.current_url
            
            if "account.live.com" in current_url or "outlook.live.com" in current_url or "mail.live.com" in current_url:
                print("🎉 ĐĂNG KÝ THÀNH CÔNG!")
                return True
            else:
                print("⚠️ Cần kiểm tra thủ công...")
                # Vẫn trả về True vì có thể đã thành công
                return True
                
        except Exception as e:
            print(f"⚠️ Lỗi trong quá trình hoàn tất: {e}")
            # Vẫn tiếp tục vì có thể đã thành công
            return True

    def verify_and_login(self, email, password):
        """Xác minh đăng nhập thành công"""
        try:
            print("9. Đang xác minh đăng nhập...")
            
            # Truy cập trực tiếp đến Outlook
            self.driver.get("https://outlook.live.com/mail/")
            self.random_delay(5, 7)
            
            # Kiểm tra xem đã đăng nhập chưa
            current_url = self.driver.current_url
            page_source = self.driver.page_source
            
            if "inbox" in current_url.lower() or "mail" in current_url.lower():
                print("✅ Đã tự động đăng nhập thành công!")
                return True
                
            # Nếu chưa đăng nhập, thử đăng nhập thủ công
            print("🔄 Thử đăng nhập thủ công...")
            
            # Tìm field email và điền
            email_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "loginfmt"))
            )
            email_field.clear()
            email_field.send_keys(email)
            self.random_delay(1, 2)
            
            # Click Next
            next_btn = self.driver.find_element(By.ID, "idSIButton9")
            next_btn.click()
            self.random_delay(3, 5)
            
            # Điền password
            password_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "passwd"))
            )
            password_field.clear()
            password_field.send_keys(password)
            self.random_delay(1, 2)
            
            # Click Sign in
            signin_btn = self.driver.find_element(By.ID, "idSIButton9")
            signin_btn.click()
            self.random_delay(5, 7)
            
            # Kiểm tra kết quả đăng nhập
            time.sleep(5)
            if "inbox" in self.driver.current_url.lower() or "mail" in self.driver.current_url.lower():
                print("✅ Đăng nhập thủ công thành công!")
                return True
            else:
                print("⚠️ Đăng nhập cần xác minh bổ sung")
                return False
                
        except Exception as e:
            print(f"⚠️ Lỗi xác minh đăng nhập: {e}")
            return False

    def fill_signup_form(self, email=None, password=None):
        """Điền form đăng ký Hotmail hoàn chỉnh, cho phép truyền email/password bên ngoài vào"""
        try:
            print("📝 Bắt đầu điền form đăng ký...")
            self.driver.get("https://signup.live.com/")
            self.random_delay(3, 5)
            # Nếu không truyền vào thì tự sinh
            if email is None or password is None:
                username = self.generate_username()
                password = self.generate_password()
                email = f"{username}@outlook.com"
            print(f"👤 Username: {email.split('@')[0]}")
            print(f"🔑 Password: {password}")
            print(f"📧 Email sẽ tạo: {email}")
            # Bước 1: Xử lý trang Email/Username
            self.dismiss_overlays_and_cookies()
            try:
                self.driver.switch_to.default_content()
            except Exception:
                pass
            username_candidates = [
                (By.NAME, "MemberName"),
                (By.ID, "MemberName"),
                (By.CSS_SELECTOR, "input[name='MemberName']"),
                (By.CSS_SELECTOR, "input[type='email']"),
                (By.XPATH, "//input[@name='MemberName' or @id='MemberName']")
            ]
            filled_username = self.send_keys_any(username_candidates, email, "Email/Username")
            if not filled_username:
                clicked_new_email = self.click_any([
                    (By.ID, "liveSwitch"),
                    (By.XPATH, "//a[contains(., 'Get a new email address')]"),
                    (By.XPATH, "//button[contains(., 'Tạo email mới')]")
                ], "Tạo email mới")
                filled_username = self.send_keys_any(username_candidates, email, "Email/Username")
                if not filled_username:
                    raise Exception("Không tìm thấy/điền được trường Email (MemberName)")
                
            # Bước 2: Chọn @outlook.com nếu có
            if self.is_present(By.XPATH, "//option[@value='outlook.com']", timeout=2):
                self.wait_and_click(By.XPATH, "//option[@value='outlook.com']", "Chọn @outlook.com")
            elif self.is_present(By.NAME, "Domain", timeout=2):
                try:
                    domain_select = self.wait.until(EC.presence_of_element_located((By.NAME, "Domain")))
                    Select(domain_select).select_by_value("outlook.com")
                    self.random_delay(0.5, 1)
                except Exception:
                    pass
            # Bước 3: Điền lại Email/Username (full email)
            self.wait_and_send_keys(By.NAME, "MemberName", email, "Email/Username")
            # Bước 4: Click Next
            next_candidates = [
                (By.ID, "iSignupAction"),
                (By.XPATH, "//input[@type='submit' and (contains(@value,'Next') or contains(@value,'Tiếp'))]"),
                (By.XPATH, "//button[contains(., 'Next') or contains(., 'Tiếp')]")
            ]
            if not self.click_any(next_candidates, "Next"):
                if not self.press_enter_on(username_candidates, "Enter Next"):
                    if not self.submit_parent_form(username_candidates):
                        raise Exception("Không click/submit được nút Next sau bước Email")
                    
            # Đợi màn Password xuất hiện
            if not self.wait_for_any([(By.ID, "PasswordInput"), (By.NAME, "passwd"), (By.CSS_SELECTOR, "input[type='password']")], timeout=10):
                self.click_any(next_candidates, "Next retry")
                if not self.wait_for_any([(By.ID, "PasswordInput"), (By.NAME, "passwd")], timeout=8):
                    raise Exception("Không chuyển sang màn hình nhập mật khẩu sau khi bấm Next")
            self.random_delay(2, 3)
            
            # Bước 5-6: Điền password và chuyển tiếp
            self.fill_password_fast_and_next(password)
            self.random_delay(1, 2)
            
            # Bước 7: Điền thông tin Birthdate (không click Next ở đây)
            if not self.select_country_and_birthdate():
                raise Exception("Điền thông tin Birthdate thất bại")
                
            # Chờ đến khi form điền tên xuất hiện (ví dụ: trường firstNameInput)
            if self.wait_for_any([(By.NAME, "firstNameInput"), (By.ID, "firstNameInput")], timeout=10):
                print("[INFO] Form điền tên đã hiện.")
            else:
                raise Exception("Không tìm thấy form điền FirstName sau khi điền Birthdate.")
            
            # Bước 8: Điền thông tin bổ sung (First Name và Last Name)
            self.auto_fill_additional_info()
            
            # Bước 9: Thực hiện xác minh người dùng bằng cách nhấn và giữ nút 'Press and hold'
            if not self.press_and_hold_verification():
                raise Exception("Không thực hiện được nhấn và giữ 'Press and hold'")
            
            # Bước 10: Click Next để đến CAPTCHA
            if not self.wait_and_click(By.ID, "iSignupAction", "Next đến CAPTCHA"):
                raise Exception("Không click được nút Next đến CAPTCHA")
            self.random_delay(3, 5)
            
            print("✅ Đã điền xong form, sẵn sàng cho CAPTCHA!")
            return email, password

        except Exception as e:
            print(f"❌ Lỗi điền form: {e}")
            try:
                self.driver.save_screenshot("error.png")
                print("📸 Đã lưu ảnh lỗi: error.png")
            except Exception:
                pass
            return None, None

    def save_account(self, email, password, status="success"):
        """Lưu thông tin tài khoản vào file"""
        try:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("hotmail_accounts.txt", "a", encoding="utf-8") as f:
                f.write(f"Email: {email}\n")
                f.write(f"Password: {password}\n")
                f.write(f"Status: {status}\n")
                f.write(f"Created: {timestamp}\n")
                f.write("-" * 50 + "\n")
            print(f"✅ Đã lưu tài khoản vào hotmail_accounts.txt")
            
            # In ra console để dễ copy
            print("\n" + "🎯" * 20)
            print("THÔNG TIN TÀI KHOẢN:")
            print(f"📧 Email: {email}")
            print(f"🔑 Password: {password}")
            print(f"📊 Status: {status}")
            print("🎯" * 20)
            
        except Exception as e:
            print(f"❌ Lỗi lưu file: {e}")

    def create_account(self, email=None, password=None):
        """Tạo một tài khoản Hotmail hoàn chỉnh. Trả về (email, password) nếu thành công, (None, None) nếu thất bại. Có thể truyền email/password bên ngoài vào."""
        try:
            if not self.setup_driver():
                return None, None
            email, password = self.fill_signup_form(email=email, password=password)
            if not email:
                print("❌ Không thể điền form đăng ký")
                return None, None
            self.solve_captcha_manually()
            if self.complete_verification():
                login_success = self.verify_and_login(email, password)
                if login_success:
                    self.save_account(email, password, "SUCCESS")
                    print(f"\n🎉 TẠO TÀI KHOẢN THÀNH CÔNG: {email}")
                    return email, password
                else:
                    self.save_account(email, password, "NEEDS_MANUAL_LOGIN")
                    print(f"\n⚠️ Tài khoản được tạo nhưng cần đăng nhập thủ công: {email}")
                    return email, password
            else:
                self.save_account(email, password, "FAILED")
                print(f"\n❌ Tạo tài khoản thất bại: {email}")
                return None, None
        except Exception as e:
            print(f"❌ Lỗi tạo tài khoản: {e}")
            return False
        finally:
            if self.driver:
                print("\n🔄 Trình duyệt sẽ đóng sau 10 giây...")
                time.sleep(10)
                self.driver.quit()
                print("✅ Đã đóng trình duyệt!")

    def select_country_and_birthdate(self):
        """Chọn khu vực (Country) và điền thông tin ngày sinh từ combobox (Tháng, Ngày) và input (Năm)"""
        try:
            print("6. Đang điền thông tin bổ sung (khu vực và ngày sinh)...")
            
            # Đợi form xuất hiện
            try:
                self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@name='Country' or @name='BirthDay' or @name='BirthMonth' or @name='BirthYear']")))
            except Exception:
                pass

            # Tạo dữ liệu ngày sinh
            day, month_num, year = self.generate_birthdate()  # Đổi tên biến month thành month_num
            month_names = ["", "January", "February", "March", "April", "May", "June", 
                           "July", "August", "September", "October", "November", "December"]
            month_name = month_names[month_num]  # Tên tháng dạng text

            # Chọn khu vực (Country)
            try:
                country_el = None
                for by, val in [
                    (By.NAME, "Country"),
                    (By.CSS_SELECTOR, "select[name='Country']"),
                ]:
                    els = self.driver.find_elements(by, val)
                    if els:
                        country_el = els[0]
                        break
                if country_el:
                    try:
                        Select(country_el).select_by_visible_text("Vietnam")
                    except Exception:
                        self.driver.execute_script(
                            "arguments[0].value='VN'; arguments[0].dispatchEvent(new Event('change',{bubbles:true}));", country_el)
                    current_val = country_el.get_attribute('value')
                    if current_val not in ['VN', 'Vietnam', 'Viet Nam']:
                        print("[WARNING] Chọn Country có thể chưa chính xác.")
            except Exception:
                pass

            self.random_delay(0.3, 0.6)
            
            # --- Cố gắng chọn Tháng và Ngày bằng cách Click Combobox/Select/Fallback ---
            if self.driver.find_elements(By.XPATH, "//*[@role='combobox' and contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'month')]") \
               and self.driver.find_elements(By.XPATH, "//*[@role='combobox' and contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'day')]"):
                
                print("[DATE] Chọn Tháng và Ngày qua aria-combobox (Click)")
                if not self.auto_select_combobox_click_option("month"): 
                    print("[WARNING] Chọn Tháng combobox thất bại, đang điền bằng input")
                    self.wait_and_send_keys(By.NAME, "BirthMonth", str(month_num), "BirthMonth")
                if not self.auto_select_combobox_click_option("day"):
                    print("[WARNING] Chọn Ngày combobox thất bại, đang điền bằng input")
                    self.wait_and_send_keys(By.NAME, "BirthDay", str(day), "BirthDay")
            elif self.is_present(By.NAME, "BirthMonth", timeout=2) and self.is_present(By.NAME, "BirthDay", timeout=2):
                print("[DATE] Chọn Tháng và Ngày qua <select> tag (Select object/Click)")
                try:
                    Select(self.driver.find_element(By.NAME, "BirthMonth")).select_by_value(str(month_num))
                    print("[INFO] Đã chọn Month qua Select (Click)")
                except:
                    print("[WARNING] Chọn Month qua Select thất bại, dùng input")
                    self.wait_and_send_keys(By.NAME, "BirthMonth", str(month_num), "BirthMonth")
                try:
                    Select(self.driver.find_element(By.NAME, "BirthDay")).select_by_value(str(day))
                    print("[INFO] Đã chọn Day qua Select (Click)")
                except:
                    print("[WARNING] Chọn Day qua Select thất bại, dùng input")
                    self.wait_and_send_keys(By.NAME, "BirthDay", str(day), "BirthDay")
            else:
                print("[DATE] Fallback: Dùng send_keys cho Month, Day, Year")
                self.wait_and_send_keys(By.NAME, "BirthDay", str(day), "BirthDay")
                self.wait_and_send_keys(By.NAME, "BirthMonth", str(month_num), "BirthMonth")
            
            self.wait_and_send_keys(By.NAME, "BirthYear", str(year), "BirthYear")
            self.random_delay(0.5, 1)
            
            # Tự động click nút Next sau khi điền xong thông tin
            next_candidates = [
                (By.ID, "iSignupAction"),
                (By.XPATH, "//button[@data-testid='primaryButton' and contains(., 'Next')]")
            ]
            if self.click_any(next_candidates, "Next sau Birthdate"):
                self.random_delay(1, 2)
            
            print("✅ Đã điền xong thông tin bổ sung")
            return True

        except Exception as e:
            print(f"❌ Lỗi điền thông tin bổ sung: {e}")
            return False

    def auto_select_combobox_click_option(self, label, option_value=None):
        """
        Click vào combobox được định danh bởi label hoặc id nếu có.
        Sau khi click, đợi dropdown mở ra và chọn 1 option (theo option_value nếu truyền vào, nếu không chọn ngẫu nhiên).
        """
        try:
            # Nếu label là "month", ưu tiên tìm nút với id 'BirthMonthDropdown'
            if label.lower() == "month":
                combo = self.wait.until(EC.element_to_be_clickable((By.ID, "BirthMonthDropdown")))
            else:
                combo = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, f"//*[@role='combobox' and contains(translate(@aria-label, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), '{label.lower()}')]")
                ))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", combo)
            
            try:
                combo.click()
            except Exception:
                # Sử dụng ActionChains nếu click trực tiếp không được
                ActionChains(self.driver).move_to_element(combo).click().perform()
            
            # Chờ thuộc tính aria-expanded chuyển thành "true" (nếu có)
            try:
                self.wait.until(lambda d: combo.get_attribute("aria-expanded") == "true")
            except Exception:
                time.sleep(0.5)
            self.random_delay(0.5, 1)
            
            # Chờ container dropdown hiển thị
            listbox = WebDriverWait(self.driver, 8).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@role='listbox']"))
            )
            
            # Lấy danh sách các option từ dropdown
            options = listbox.find_elements(By.XPATH, ".//*[@role='option']")
            print(f"[DEBUG] Số lượng option tìm được cho '{label}': {len(options)}")
            if not options:
                print(f"[ERROR] Không tìm thấy option trong dropdown của combobox {label}")
                return False
            
            # Chọn option: nếu có option_value thì tìm kiếm theo text, nếu không chọn ngẫu nhiên
            if option_value:
                selected_option = next((opt for opt in options if opt.text.strip() == option_value), None)
            else:
                selected_option = random.choice(options)
            
            if not selected_option:
                print(f"[ERROR] Không tìm thấy option '{option_value}' cho combobox {label}")
                return False
            
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", selected_option)
            try:
                selected_option.click()
            except Exception:
                try:
                    ActionChains(self.driver).move_to_element(selected_option).click().perform()
                except Exception:
                    self.driver.execute_script("arguments[0].click();", selected_option)
            self.random_delay(0.5, 1)
            
            # Đợi cho dropdown đóng lại (nếu thuộc tính aria-expanded thay đổi)
            try:
                self.wait.until(lambda d: combo.get_attribute("aria-expanded") == "false")
            except Exception:
                pass
            return True
        except Exception as e:
            print(f"[ERROR] Lỗi khi chọn combobox {label}: {e}")
            return False
    def auto_fill_additional_info(self):
        """Tự động điền thông tin bổ sung (First Name và Last Name) và click Next"""
        try:
            print("7. Điền thông tin bổ sung (First Name và Last Name)...")
            first_names = ["John", "Alice", "Bob", "Jane", "Mike", "Emily"]
            last_names = ["Smith", "Doe", "Johnson", "Williams", "Brown"]
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            # Sử dụng selector mới cho First Name
            if self.is_present(By.NAME, "firstNameInput", timeout=2):
                self.wait_and_send_keys(By.NAME, "firstNameInput", first_name, "First Name")
            elif self.is_present(By.ID, "firstNameInput", timeout=2):
                self.wait_and_send_keys(By.ID, "firstNameInput", first_name, "First Name")
            # Sử dụng selector mới cho Last Name
            if self.is_present(By.NAME, "lastNameInput", timeout=2):
                self.wait_and_send_keys(By.NAME, "lastNameInput", last_name, "Last Name")
            elif self.is_present(By.ID, "lastNameInput", timeout=2):
                self.wait_and_send_keys(By.ID, "lastNameInput", last_name, "Last Name")
            # Click Next để chuyển sang CAPTCHA hoặc bước tiếp theo
            next_candidates = [
                (By.ID, "iSignupAction"),
                (By.XPATH, "//button[@data-testid='primaryButton' and contains(., 'Next')]")
            ]
            if self.click_any(next_candidates, "Next sau Điền thông tin bổ sung"):
                self.random_delay(1, 2)
            print("✅ Đã điền xong thông tin bổ sung (First Name và Last Name).")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi điền thông tin bổ sung: {e}")
            return False

    def press_and_hold_verification(self):
        """Nhấn và giữ nút 'Press and hold' để xác minh người dùng"""
        try:
            print("8. Đang thực hiện xác minh: nhấn và giữ 'Press and hold'")
            # Chờ cho đến khi phần tử có id "UXxBnYaFLhyqAej" xuất hiện
            element = self.wait.until(EC.presence_of_element_located((By.ID, "UXxBnYaFLhyqAej")))
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
            # Sử dụng ActionChains để click và giữ trong 2 giây rồi thả ra
            ActionChains(self.driver).click_and_hold(element).pause(2).release().perform()
            self.random_delay(1, 2)
            print("✅ Đã nhấn và giữ 'Press and hold'")
            return True
        except Exception as e:
            print(f"❌ Lỗi khi nhấn giữ 'Press and hold': {e}")
            return False


def create_account_thread():
    creator = HotmailAutoCreator(fast=True)
    success = creator.create_account()
    if success:
        print("\n✅ HOÀN THÀNH! Kiểm tra file hotmail_accounts.txt")
    else:
        print("\n❌ THẤT BẠI! Vui lòng thử lại")

class MultiHotmailGUI:

    def __init__(self):
        import tkinter as tk
        from tkinter import ttk
        self.window = tk.Tk()
        self.window.title("Auto hotmail registration")
        self.window.geometry("600x400")
        self.create_widgets()
        # Danh sách lưu thông tin tài khoản
        self.account_list = []

    def create_widgets(self):
        from tkinter import ttk
        label = ttk.Label(self.window, text="Số lượng cửa sổ cần mở:")
        label.pack(pady=10)

        self.num_windows = ttk.Entry(self.window)
        self.num_windows.pack(pady=5)
        self.num_windows.insert(0, "1")

        self.fast_mode = tk.BooleanVar()
        fast_check = ttk.Checkbutton(self.window, text="Fast Mode (Tối ưu tốc độ)", variable=self.fast_mode)
        fast_check.pack(pady=5)

        # Frame chứa các nút điều khiển
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=5)
        
        start_button = ttk.Button(button_frame, text="Bắt đầu", command=self.start_creation)
        start_button.pack(side="left", padx=5)
        
        stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_creation)
        stop_button.pack(side="left", padx=5)
        
        delete_button = ttk.Button(button_frame, text="Delete", command=self.delete_selected)
        delete_button.pack(side="left", padx=5)

        # Thêm bảng hiển thị tài khoản
        self.tree = ttk.Treeview(self.window, columns=("stt", "email", "password"), show="headings", height=8)
        self.tree.heading("stt", text="STT")
        self.tree.heading("email", text="Email")
        self.tree.heading("password", text="Password")
        self.tree.column("stt", width=50, anchor="center")
        self.tree.column("email", width=220, anchor="w")
        self.tree.column("password", width=180, anchor="w")
        self.tree.pack(pady=10, fill="x")

    def add_account_to_table(self, email, password):
        stt = len(self.account_list) + 1
        self.account_list.append((email, password))
        self.tree.insert("", "end", values=(stt, email, password))


    def stop_creation(self):
        """Dừng quá trình tạo tài khoản"""
        self.running = False
        print("⛔ Đang dừng quá trình tạo tài khoản...")
        
    def delete_selected(self):
        """Xóa tài khoản đã chọn khỏi bảng"""
        selected_items = self.tree.selection()
        if not selected_items:
            print("⚠️ Vui lòng chọn tài khoản cần xóa!")
            return
            
        for item in selected_items:
            values = self.tree.item(item)['values']
            if values:
                # Xóa khỏi account_list
                email = values[1]  # email ở cột thứ 2
                self.account_list = [(e, p) for e, p in self.account_list if e != email]
                # Xóa khỏi bảng
                self.tree.delete(item)
        
        # Cập nhật lại STT
        for idx, item in enumerate(self.tree.get_children(), 1):
            self.tree.set(item, "stt", idx)
            
    def start_creation(self):
        try:
            if self.running:
                print("⚠️ Đang trong quá trình tạo tài khoản!")
                return
                
            num = int(self.num_windows.get())
            if num <= 0:
                print("Số lượng cửa sổ phải lớn hơn 0")
                return

            self.running = True
            print("🔥 HOTMAIL AUTO CREATOR - GUI VERSION")
            print("=" * 60)
            print(f"Bắt đầu tạo {num} tài khoản Hotmail...")
            print("=" * 60)

            fast_mode_val = self.fast_mode.get()
            def worker(fast_mode):
                creator = HotmailAutoCreator(fast=fast_mode)
                try:
                    if not self.running:
                        return
                    username = creator.generate_username()
                    password = creator.generate_password()
                    email = f"{username}@outlook.com"
                    self.window.after(0, self.add_account_to_table, email, password)
                    # Truyền đúng email/password vào quá trình tạo tài khoản
                    creator.create_account(email=email, password=password)
                except Exception as e:
                    print(f"Không thể cập nhật bảng: {e}")
                finally:
                    if creator and creator.driver:
                        creator.driver.quit()

            threads = []
            for _ in range(num):
                t = threading.Thread(target=worker, args=(fast_mode_val,))
                threads.append(t)
                t.start()
                time.sleep(1)

            print(f"Đã bắt đầu tạo {num} tài khoản...")

        except ValueError:
            print("Vui lòng nhập số hợp lệ")
    
    def __init__(self):
        import tkinter as tk
        from tkinter import ttk
        self.window = tk.Tk()
        self.window.title("Tạo nhiều tài khoản Hotmail")
        self.window.geometry("600x400")
        # Thêm biến để kiểm soát threads
        self.running = False
        self.threads = []
        self.create_widgets()
        # Danh sách lưu thông tin tài khoản
        self.account_list = []
        
    def run(self):
        self.window.mainloop()

def main():
    app = MultiHotmailGUI()
    app.run()

if __name__ == "__main__":
    main()