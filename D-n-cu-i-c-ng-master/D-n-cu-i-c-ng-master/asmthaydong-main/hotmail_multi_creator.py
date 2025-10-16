from hotmail_auto_simple import HotmailAutoCreator
import threading
import tkinter as tk
from tkinter import ttk
import sys

class MultiHotmailCreator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tạo nhiều tài khoản Hotmail")
        self.window.geometry("400x200")
        
        # Tạo giao diện
        self.create_widgets()
        
    def create_widgets(self):
        # Label và input cho số lượng cửa sổ
        label = ttk.Label(self.window, text="Số lượng cửa sổ cần mở:")
        label.pack(pady=10)
        
        self.num_windows = ttk.Entry(self.window)
        self.num_windows.pack(pady=5)
        self.num_windows.insert(0, "1")  # Giá trị mặc định
        
        # Checkbox fast mode
        self.fast_mode = tk.BooleanVar()
        fast_check = ttk.Checkbutton(self.window, text="Fast Mode (Tối ưu tốc độ)", 
                                   variable=self.fast_mode)
        fast_check.pack(pady=5)
        
        # Nút Start
        start_button = ttk.Button(self.window, text="Bắt đầu", command=self.start_creation)
        start_button.pack(pady=20)
        
    def create_account(self, fast_mode):
        """Hàm tạo một tài khoản trong một luồng riêng"""
        creator = HotmailAutoCreator(fast=fast_mode)
        try:
            creator.setup_driver()
            creator.create_account()
        except Exception as e:
            print(f"Lỗi khi tạo tài khoản: {str(e)}")
        
    def start_creation(self):
        try:
            num = int(self.num_windows.get())
            if num <= 0:
                print("Số lượng cửa sổ phải lớn hơn 0")
                return
                
            # Tạo và khởi chạy các luồng
            threads = []
            for _ in range(num):
                thread = threading.Thread(
                    target=self.create_account,
                    args=(self.fast_mode.get(),)
                )
                thread.daemon = True  # Thoát thread khi chương trình kết thúc
                threads.append(thread)
                thread.start()
                
            # Thông báo
            print(f"Đã bắt đầu tạo {num} tài khoản...")
            
        except ValueError:
            print("Vui lòng nhập số hợp lệ")
        
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = MultiHotmailCreator()
    app.run()