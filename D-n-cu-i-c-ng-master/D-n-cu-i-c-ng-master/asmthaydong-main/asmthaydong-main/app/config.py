import os

DB_PATH = os.path.join(os.path.dirname(__file__), "accounts.db")

# Proxy list file (http://user:pass@host:port or socks5://user:pass@host:port)
PROXY_LIST_PATH = os.path.join(os.path.dirname(__file__), "proxies.txt")

# Default provider domain
OUTLOOK_DOMAIN = "outlook.com"

# Captcha provider key placeholders
CAPTCHA_API_KEY = os.getenv("CAPTCHA_API_KEY", "")




