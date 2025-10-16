## Auto Email Register & Warm-up (Outlook/Gmail) with Proxy Rotation

This project automates account creation and basic warm-up actions for Outlook (and Gmail stub) with proxy rotation and an anti-detect browser.

### Quick start

1) Install Python 3.10+
2) Install requirements:
```
pip install -r requirements.txt
```
3) CLI usage:
```
# Create 1 Outlook account (manual captcha)
python -m app.cli create --provider outlook --count 1

# Warm-up last 1 account
python -m app.cli warmup --provider outlook --count 1

# List accounts
python -m app.cli list --limit 20
```

### Structure
```
app/
  __init__.py
  config.py
  db.py                # SQLite repository
  proxies.py           # proxy rotation & validation
  browser.py           # undetected-chromedriver launcher
  outlook_signup.py    # Outlook registration flow (manual/2captcha hook)
  gmail_signup.py      # Gmail stub
  warmup.py            # warm-up routines for Outlook
  cli.py               # command-line entry
```

### Notes
- This is for learning/research only. Do not use for abuse/spam.
- Residential/4G proxies are strongly recommended.
- Captcha is manual by default; integrate 2Captcha/Anti-Captcha where marked.




