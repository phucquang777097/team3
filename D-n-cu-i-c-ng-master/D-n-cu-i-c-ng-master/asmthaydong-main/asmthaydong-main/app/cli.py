import argparse
from rich import print

from .db import init_db, insert_account, list_accounts, update_status
from .proxies import choose_proxy, verify_proxy
from .browser import build_chrome
from .outlook_signup import create_outlook_account
from .gmail_signup import create_gmail_account
from .warmup import outlook_warmup


def cmd_create(provider: str, count: int, headless: bool):
    init_db()
    for i in range(count):
        proxy = choose_proxy()
        if proxy and not verify_proxy(proxy):
            print(f"[yellow]Proxy seems invalid, skipping: {proxy}")
            proxy = None

        if provider == "outlook":
            email, password = create_outlook_account(proxy=proxy, headless=headless)
        else:
            email, password = create_gmail_account(proxy=proxy, headless=headless)

        if email and password:
            insert_account(provider, email, password, None, proxy, None, status="created")
            print(f"[green]Created: {email}")
        else:
            print(f"[red]Failed to create {provider} account")


def cmd_list(provider: str, limit: int):
    init_db()
    rows = list_accounts(limit=limit, provider=provider or None)
    for r in rows:
        print(r)


def cmd_warmup(provider: str, count: int, headless: bool):
    init_db()
    rows = list_accounts(limit=count, provider=provider)
    for r in rows:
        email = r["email"]
        password = r["password"]
        if provider == "outlook":
            ok = outlook_warmup(email, password, proxy=None, headless=headless)
            update_status(email, "warmed" if ok else "warm_failed")
            print(f"[green]Warmed: {email}" if ok else f"[red]Warm-up failed: {email}")


def main():
    parser = argparse.ArgumentParser(description="Auto Email Register & Warm-up")
    sub = parser.add_subparsers(dest="cmd")

    c = sub.add_parser("create")
    c.add_argument("--provider", choices=["outlook", "gmail"], default="outlook")
    c.add_argument("--count", type=int, default=1)
    c.add_argument("--headless", action="store_true")

    l = sub.add_parser("list")
    l.add_argument("--provider", choices=["outlook", "gmail"], default=None)
    l.add_argument("--limit", type=int, default=20)

    w = sub.add_parser("warmup")
    w.add_argument("--provider", choices=["outlook", "gmail"], default="outlook")
    w.add_argument("--count", type=int, default=1)
    w.add_argument("--headless", action="store_true")

    args = parser.parse_args()
    if args.cmd == "create":
        cmd_create(args.provider, args.count, args.headless)
    elif args.cmd == "list":
        cmd_list(args.provider, args.limit)
    elif args.cmd == "warmup":
        cmd_warmup(args.provider, args.count, args.headless)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()




