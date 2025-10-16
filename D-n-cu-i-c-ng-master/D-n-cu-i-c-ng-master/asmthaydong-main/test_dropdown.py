from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

class DropdownTester:
    def __init__(self):
        self.driver = None
        self.wait = None

    def setup_driver(self):
        print("🚀 Đang khởi động Chrome...")
        try:
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            options.add_argument('--start-maximized')
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 15)
            return True
        except Exception as e:
            print(f"❌ Lỗi khởi động Chrome: {e}")
            return False

    def test_dropdown(self):
        try:
            self.driver.get("https://signup.live.com/signup")
            time.sleep(3)

            # Lưu screenshot và page source ngay sau khi load trang để tránh mất kết nối
            try:
                print("DEBUG: Bắt đầu lưu screenshot ngay sau load trang")
                screenshot_path = os.path.join(os.getcwd(), "dropdown_debug.png")
                html_path = os.path.join(os.getcwd(), "dropdown_debug.html")
                self.driver.save_screenshot(screenshot_path)
                with open(html_path, "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
                print(f"Đã lưu screenshot: {screenshot_path}")
                print(f"Đã lưu page source: {html_path}")
            except Exception as e:
                print(f"Không thể lưu screenshot/html: {e}")
            time.sleep(1)

            # Thử tìm các selector phổ biến cho trường email / username để chẩn đoán
            selectors = [
                (By.NAME, 'MemberName'),
                (By.ID, 'MemberName'),
                (By.NAME, 'email'),
                (By.XPATH, "//input[@type='email']"),
                (By.XPATH, "//input[contains(translate(@placeholder,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'email') or contains(translate(@placeholder,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'địa chỉ email')]")
            ]
            for sel in selectors:
                try:
                    elems = self.driver.find_elements(sel[0], sel[1])
                    print(f"Selector {sel}: found {len(elems)}")
                    if elems:
                        print(f" - OuterHTML snippet: {elems[0].get_attribute('outerHTML')[:300]}")
                except Exception as e:
                    print(f" - Error checking {sel}: {e}")

            # Nếu tồn tại email input, thử gửi và tiến hành bước tiếp
            try:
                email_elem = None
                for sel in selectors:
                    elems = self.driver.find_elements(sel[0], sel[1])
                    if elems:
                        email_elem = elems[0]
                        break
                if email_elem:
                    email_elem.send_keys("test1234567890xyz@outlook.com")
                    try:
                        next_button = self.driver.find_element(By.ID, "iSignupAction")
                        next_button.click()
                        print("Đã click Next")
                        time.sleep(3)
                    except Exception as e:
                        print(f"Không tìm/không click được nút Next: {e}")
                else:
                    print("Không tìm thấy trường email trên trang signup (có thể do popup/CAPTCHA/redirect).")
            except Exception as e:
                print(f"Lỗi khi thao tác với trường email: {e}")

            # In ra phần HTML gần vùng dropdown để debug
            try:
                # Tìm phần chứa dropdown
                container = self.driver.find_element(By.XPATH, "//label[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'tháng') or contains(translate(.,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'month')]/..")
                print("Found container for 'month' label. Inner HTML snippet:")
                print(container.get_attribute('innerHTML')[:2000])
            except Exception as e:
                print(f"Không tìm được container label month: {e}")

            # Tìm dropdown button theo id
            try:
                print("Tìm element id=BirthMonthDropdown")
                el = self.driver.find_element(By.ID, "BirthMonthDropdown")
                print("Found BirthMonthDropdown. OuterHTML snippet:")
                print(el.get_attribute('outerHTML')[:2000])
            except Exception as e:
                print(f"Không tìm được BirthMonthDropdown: {e}")

            # In ra options theo role
            try:
                options = self.driver.find_elements(By.XPATH, "//div[@role='option']")
                print(f"Các option (count): {len(options)}")
                for o in options:
                    print(f"- data-value={o.get_attribute('data-value')} text={o.text}")
            except Exception as e:
                print(f"Không lấy được options: {e}")

            time.sleep(5)
        except Exception as e:
            print(f"Lỗi chung khi test dropdown: {e}")
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == '__main__':
    t = DropdownTester()
    if t.setup_driver():
        t.test_dropdown()