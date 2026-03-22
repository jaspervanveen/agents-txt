#!/usr/bin/env python3
"""
Monitor HN thread for new comments and report via Telegram.
Thread: https://news.ycombinator.com/item?id=47314984
"""

import json
import os
import urllib.request

ITEM_ID     = 47314984
SEEN_FILE   = os.path.join(os.path.dirname(__file__), "hn_seen_comments.json")
TELEGRAM_TOKEN   = "8609324880:AAGaPqFRkACjY3NuYL_NWu9rq-vmwbDuAbc"
TELEGRAM_CHAT_ID = "6806784691"
HN_API = "https://hacker-news.firebaseio.com/v0"

def load_seen():
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE) as f:
            return set(json.load(f))
    return set()

def save_seen(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)

def fetch(url):
    with urllib.request.urlopen(url, timeout=10) as r:
        return json.loads(r.read())

def get_comment(cid):
    try:
        return fetch(f"{HN_API}/item/{cid}.json")
    except Exception:
        return None

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }).encode()
    req = urllib.request.Request(url, data=payload,
                                  headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def main():
    seen = load_seen()
    item = fetch(f"{HN_API}/item/{ITEM_ID}.json")
    all_kids = item.get("kids", [])

    new_comments = []
    for cid in all_kids:
        if cid in seen:
            continue
        c = get_comment(cid)
        if not c or c.get("dead") or c.get("deleted"):
            seen.add(cid)
            continue
        new_comments.append(c)
        seen.add(cid)

    if new_comments:
        lines = [f"💬 *{len(new_comments)} new comment(s)* on your agents.txt HN thread:\n"]
        for c in new_comments:
            author = c.get("by", "unknown")
            text = c.get("text", "")
            # Strip HTML tags roughly
            import re
            text = re.sub(r"<[^>]+>", "", text)
            text = text[:280] + ("…" if len(text) > 280 else "")
            lines.append(f"*{author}:*\n{text}\n")
        lines.append(f"🔗 https://news.ycombinator.com/item?id={ITEM_ID}")
        send_telegram("\n".join(lines))

    save_seen(seen)
    print(f"Done. {len(new_comments)} new, {len(seen)} total seen.")

if __name__ == "__main__":
    main()
