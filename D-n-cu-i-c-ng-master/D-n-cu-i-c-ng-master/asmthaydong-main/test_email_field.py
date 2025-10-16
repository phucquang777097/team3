from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

def setup_driver():
    """Khởi tạo Chrome driver với các tùy chọn chống phát hiện automation"""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    
    # Cơ bản
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Thêm các tùy chọn để giả lập người dùng thật
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(service=service, options=options)
    
    # Thêm JavaScript để ghi đè các thuộc tính phát hiện automation
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

def enter_email_like_human(driver, email):
    """Điền email với độ trễ như người thật"""
    try:
        # Đợi và tìm input email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "MemberName"))
        )
        
        print(f"Tìm thấy input email, đang điền: {email}")
        
        # Di chuyển chuột đến input và click
        action = ActionChains(driver)
        action.move_to_element(email_input).click().perform()
        time.sleep(1)
        
        # Điền từng ký tự với độ trễ ngẫu nhiên
        for char in email:
            email_input.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))
        
        print("Đã điền email xong, đợi 1 giây...")
        time.sleep(1)
        
        # Click nút Next
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "iSignupAction"))
        )
        
        print("Tìm thấy nút Next, đang click...")
        action.move_to_element(next_button).click().perform()
        
        # Đợi để xem có chuyển trang không
        time.sleep(3)
        
        # Kiểm tra xem đã chuyển trang thành công chưa
        try:
            month_dropdown = driver.find_element(By.ID, "BirthMonthDropdown")
            print("✅ Đã chuyển đến trang chọn ngày tháng thành công!")
            return True
        except:
            print("❌ Chưa chuyển đến trang chọn ngày tháng!")
            return False
            
    except Exception as e:
        print(f"Lỗi khi điền email: {str(e)}")
        return False

def main():
    driver = None
    try:
        print("🚀 Khởi động Chrome...")
        driver = setup_driver()
        
        # Mở trang đăng ký
        driver.get("https://signup.live.com/signup")
        time.sleep(3)
        
        # Điền email với hành vi giống người dùng
        email = f"test{random.randint(10000,99999)}@outlook.com"
        if enter_email_like_human(driver, email):
            print("Đã vào form chọn ngày tháng, dừng lại để kiểm tra...")
            input("Nhấn Enter để thoát...")
        else:
            print("Không thể vượt qua form email!")
            input("Nhấn Enter để thoát...")
        
    except Exception as e:
        print(f"Lỗi: {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()