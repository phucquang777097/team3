from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

def setup_driver():
    """Khởi tạo Chrome driver"""
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    return webdriver.Chrome(service=service, options=options)

def select_month_by_js(driver, month_num):
    """Chọn tháng bằng JavaScript"""
    try:
        # Click vào dropdown
        month_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "BirthMonthDropdown"))
        )
        driver.execute_script("arguments[0].click();", month_btn)
        time.sleep(1)
        
        # Tìm và click vào option bằng JavaScript
        script = f"""
            function findAndClickOption() {{
                // Tìm tất cả các options
                var options = document.querySelectorAll('div[role="option"]');
                console.log('Tìm thấy ' + options.length + ' options');
                
                // Tìm option với giá trị mong muốn
                var targetOption = Array.from(options).find(opt => 
                    opt.getAttribute('data-value') === '{month_num}' || 
                    opt.textContent.includes('{month_num}')
                );
                
                if (targetOption) {{
                    console.log('Đã tìm thấy option: ' + targetOption.textContent);
                    targetOption.click();
                    return true;
                }}
                return false;
            }}
            return findAndClickOption();
        """
        result = driver.execute_script(script)
        print(f"Kết quả chọn tháng {month_num}: {result}")
        return result
    except Exception as e:
        print(f"Lỗi khi chọn tháng: {str(e)}")
        return False

def main():
    driver = None
    try:
        print("🚀 Khởi động Chrome...")
        driver = setup_driver()
        
        # Mở trang đăng ký
        driver.get("https://signup.live.com/signup")
        time.sleep(3)
        
        # Điền email (bước cần thiết để đến form chọn ngày tháng)
        email = f"test{random.randint(10000,99999)}@outlook.com"
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "MemberName"))
        )
        email_input.send_keys(email)
        
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "iSignupAction"))
        )
        next_button.click()
        time.sleep(2)
        
        # Thử chọn các tháng từ 1-12
        for month in range(1, 13):
            print(f"\nThử chọn tháng {month}...")
            if select_month_by_js(driver, str(month)):
                print(f"✅ Đã chọn tháng {month} thành công")
                time.sleep(1)
            else:
                print(f"❌ Không chọn được tháng {month}")
        
        input("Nhấn Enter để thoát...")
        
    except Exception as e:
        print(f"Lỗi: {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()