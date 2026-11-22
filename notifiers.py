import json
import os
import textwrap
import urllib.parse
import urllib.request
from datetime import datetime
from typing import Any, Dict, List

from config import (
    APP_NAME,
    EMAIL_RECIPIENT,
    EMAIL_SENDER,
    GOOGLE_PLAY_URL,
    NTFY_SERVER,
    NTFY_TOPIC,
    RESEND_API_KEY,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
)

PLATFORM_BADGES = {
    "whatsapp": "🟢 WhatsApp",
    "facebook": "🔵 Facebook Grupa",
    "tiktok": "🎵 TikTok",
}


def print_lead(lead: Dict[str, Any]):
    flag = "🇧🇷 [BRAZYLIA]" if lead.get("country") == "BR" else "🇲🇽 [MEKSYK]"
    role = (
        "[KLIENT SZUKA FACHOWCA]"
        if lead.get("lead_type") == "SERVICE_SEEKER"
        else "[FACHOWIEC SZUKA PRACY/ZLECEŃ]"
    )
    badge = PLATFORM_BADGES.get(lead.get("platform", ""), "🌐 Social")
    print("\n" + "=" * 80)
    print(f"{flag} {role} | {badge} | {lead.get('source_channel')} | @{lead.get('author')}")
    print(f"📌 {lead.get('title')}")
    print(f"🔗 {lead.get('url')}")
    snippet = lead.get("content_snippet", "")
    if snippet:
        print(f'📄 "{textwrap.shorten(snippet, width=180, placeholder="...")}"')
    print("\n💬 Gotowa odpowiedź (zawiera link Google Play):")
    print(textwrap.fill(lead.get("ai_draft", ""), width=78))
    print("=" * 80)


def send_email_digest(leads: List[Dict[str, Any]]) -> bool:
    if not leads or not RESEND_API_KEY:
        return False

    br_count = sum(1 for l in leads if l.get("country") == "BR")
    mx_count = sum(1 for l in leads if l.get("country") == "MX")
    subject = f"📱 [{APP_NAME}] {len(leads)} leadów WhatsApp/FB/TikTok (🇧🇷 {br_count} | 🇲🇽 {mx_count})"

    cards = []
    text_lines = [f"{APP_NAME} — nowe leady (Google Play: {GOOGLE_PLAY_URL}):\n"]
    for idx, lead in enumerate(leads, 1):
        badge = PLATFORM_BADGES.get(lead.get("platform", ""), "🌐 Social")
        flag = "🇧🇷 Brazylia" if lead.get("country") == "BR" else "🇲🇽 Meksyk"
        cards.append(
            f"""
            <div style="border:1px solid #e2e8f0;border-radius:8px;padding:16px;margin-bottom:16px;">
              <div style="font-size:12px;color:#475569;margin-bottom:6px;">
                <b>{flag}</b> · <b>{badge}</b> · {lead.get('source_channel')} · @{lead.get('author')}
              </div>
              <h3 style="margin:0 0 8px 0;font-size:16px;color:#0f172a;">{lead.get('title')}</h3>
              <p style="font-size:13px;color:#475569;background:#f8fafc;padding:10px;border-radius:6px;">"{lead.get('content_snippet', '')}"</p>
              <div style="font-size:13px;background:#f0fdf4;border:1px solid #bbf7d0;padding:10px;border-radius:6px;font-family:monospace;margin:10px 0;">
                {lead.get('ai_draft', '')}
              </div>
              <a href="{lead.get('url')}" style="display:inline-block;background:#2563eb;color:#fff;padding:8px 14px;border-radius:6px;text-decoration:none;font-weight:bold;font-size:13px;">Otwórz wątek &rarr;</a>
              <a href="{GOOGLE_PLAY_URL}" style="display:inline-block;background:#16a34a;color:#fff;padding:8px 14px;border-radius:6px;text-decoration:none;font-weight:bold;font-size:13px;margin-left:8px;">Google Play</a>
            </div>
            """
        )
        text_lines.append(
            f"{idx}. [{lead.get('country')}] {badge} {lead.get('title')}\n"
            f"Link: {lead.get('url')}\n"
            f"Odpowiedź: {lead.get('ai_draft')}\n"
        )

    html_body = (
        "<html><body style='font-family:sans-serif;max-width:680px;margin:auto;padding:20px;'>"
        f"<h2>📱 {APP_NAME} — WhatsApp / Facebook / TikTok Lead Monitor</h2>"
        + "".join(cards)
        + "</body></html>"
    )

    payload = {
        "from": f"{APP_NAME} Social Bot <{EMAIL_SENDER}>",
        "to": [EMAIL_RECIPIENT],
        "subject": subject,
        "html": html_body,
        "text": "\n".join(text_lines),
    }
    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "ServiceAppSocialGroupsBot/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status in (200, 201):
                print(f"[✓] Raport e-mail wysłany przez Resend na: {EMAIL_RECIPIENT}")
                return True
    except Exception as exc:
        print(f"[!] Błąd wysyłki e-mail (Resend): {exc}")
    return False


def send_ntfy_lead(lead: Dict[str, Any]):
    if not NTFY_TOPIC:
        return
    badge = PLATFORM_BADGES.get(lead.get("platform", ""), "Social")
    url = f"{NTFY_SERVER.rstrip('/')}/{urllib.parse.quote(NTFY_TOPIC)}"
    req = urllib.request.Request(
        url,
        data=f"{lead.get('title')}\n\n{lead.get('ai_draft')}".encode("utf-8"),
        headers={
            "Title": f"{APP_NAME} [{lead.get('country')}] {badge}",
            "Click": lead.get("url") or GOOGLE_PLAY_URL,
            "Priority": "default",
        },
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=10).close()
    except Exception as exc:
        print(f"[!] Błąd ntfy: {exc}")


def send_telegram_lead(lead: Dict[str, Any]):
    if not (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID):
        return
    badge = PLATFORM_BADGES.get(lead.get("platform", ""), "Social")
    msg = (
        f"📱 {APP_NAME} [{lead.get('country')}] {badge}\n"
        f"📌 {lead.get('title')}\n"
        f"🔗 {lead.get('url')}\n\n"
        f"💬 {lead.get('ai_draft')}"
    )
    payload = urllib.parse.urlencode({"chat_id": TELEGRAM_CHAT_ID, "text": msg}).encode("utf-8")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        urllib.request.urlopen(urllib.request.Request(url, data=payload, method="POST"), timeout=10).close()
    except Exception as exc:
        print(f"[!] Błąd Telegram: {exc}")


def write_github_summary(total_scanned: int, new_leads: List[Dict[str, Any]]):
    summary_path = os.getenv("GITHUB_STEP_SUMMARY")
    if not summary_path:
        return
    lines = [
        f"# 📱 {APP_NAME} — WhatsApp / Facebook / TikTok Lead Monitor",
        "",
        f"- **Data (UTC):** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"- **Google Play:** {GOOGLE_PLAY_URL}",
        f"- **Przeanalizowano wpisów:** {total_scanned}",
        f"- **Nowych leadów:** **{len(new_leads)}**",
        "",
    ]
    if not new_leads:
        lines.append("_Brak nowych publicznych leadów w tym cyklu._")
    else:
        for idx, lead in enumerate(new_leads, 1):
            badge = PLATFORM_BADGES.get(lead.get("platform", ""), "Social")
            lines.extend(
                [
                    f"### {idx}. [{lead.get('country')}] {badge} — {lead.get('title')}",
                    f"- **Kanał:** `{lead.get('source_channel')}` | **Link:** {lead.get('url')}",
                    "```text",
                    lead.get("ai_draft", ""),
                    "```",
                    "",
                ]
            )
    try:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
    except Exception as exc:
        print(f"[!] Błąd zapisu GITHUB_STEP_SUMMARY: {exc}")
