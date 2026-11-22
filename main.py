#!/usr/bin/env python3
"""
ServiceApp Social Groups Bot — WhatsApp Groups, Facebook Groups & TikTok (BR & MX)
===================================================================================
Wkleja link Google Play (https://play.google.com/store/apps/details?id=pl.serviceapp&pli=1)
do każdej wygenerowanej odpowiedzi w PT-BR (Brazylia) i ES-MX (Meksyk).
"""

import argparse
import os
import sys
from datetime import datetime
from typing import Any, Dict, List


def load_env_file():
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


load_env_file()

from analyzer import LeadAnalyzer
from config import EMAIL_RECIPIENT, GOOGLE_PLAY_URL, WEBHOOK_PORT
from database import get_stats, init_db, is_post_seen, mark_notified, save_lead
from gemini_client import GeminiAPIError, GeminiClient
from notifiers import (
    print_lead,
    send_email_digest,
    send_ntfy_lead,
    send_telegram_lead,
    write_github_summary,
)
from sources.public_rss_monitor import PublicSocialRSSMonitor
from sources.webhook_server import start_webhook_server
from sources.whatsapp_importer import load_whatsapp_export_file


def process_items(items: List[Dict[str, Any]], analyzer: LeadAnalyzer, dry_run: bool = False) -> List[Dict[str, Any]]:
    new_leads: List[Dict[str, Any]] = []
    for item in items:
        post_id = item["id"]
        if not dry_run and is_post_seen(post_id):
            continue

        lead_type, draft = analyzer.analyze(
            title=item.get("title", ""),
            content=item.get("content", ""),
            country=item.get("country", "BR"),
            platform=item.get("platform", "whatsapp"),
        )
        if lead_type == "IRRELEVANT" or not draft:
            continue

        lead = {
            "post_id": post_id,
            "platform": item.get("platform", "whatsapp"),
            "country": item.get("country", "BR"),
            "source_channel": item.get("source_channel", ""),
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "author": item.get("author", "usuario"),
            "content_snippet": (item.get("content") or "")[:300],
            "lead_type": lead_type,
            "ai_draft": draft,
        }
        new_leads.append(lead)
        print_lead(lead)

        if not dry_run:
            save_lead(lead, notified=0)
            send_ntfy_lead(lead)
            send_telegram_lead(lead)

    if new_leads and not dry_run:
        if send_email_digest(new_leads):
            for lead in new_leads:
                mark_notified(lead["post_id"])

    return new_leads


def run_scan(mock: bool = False, dry_run: bool = False):
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 📱 ServiceApp Social Groups Bot (WhatsApp / Facebook / TikTok)")
    print(f"    Google Play: {GOOGLE_PLAY_URL}")
    init_db()
    analyzer = LeadAnalyzer()
    monitor = PublicSocialRSSMonitor()

    if mock:
        print("[i] Tryb demonstracyjny: przykładowe leady z WhatsApp, Facebook Groups i TikTok (BR & MX)...")
        items = monitor.get_mock_posts()
    else:
        print("[*] Skanowanie publicznie indeksowanych wzmianek (Facebook / TikTok / WhatsApp — BR & MX)...")
        items = monitor.scan_all()

    new_leads = process_items(items, analyzer, dry_run=dry_run)
    write_github_summary(len(items), new_leads)

    print(f"\n[✓] Zakończono skanowanie.")
    print(f"    - Przeanalizowano wpisów: {len(items)}")
    print(f"    - Wykryto leadów:         {len(new_leads)}")
    print(f"    - Odbiorca raportów:      {EMAIL_RECIPIENT}")


def main():
    parser = argparse.ArgumentParser(description="ServiceApp Social Groups Bot (WhatsApp, Facebook Groups, TikTok)")
    parser.add_argument("--dry-run", action="store_true", help="Bez zapisu do bazy i bez wysyłania powiadomień")
    parser.add_argument("--mock", action="store_true", help="Test na przykładowych leadach WhatsApp/FB/TikTok (BR & MX)")
    parser.add_argument("--webhook", action="store_true", help="Uruchamia serwer webhooków (WhatsApp/FB/TikTok) + panel HTML")
    parser.add_argument("--port", type=int, default=WEBHOOK_PORT, help="Port serwera webhooków (domyślnie 8089)")
    parser.add_argument("--import-whatsapp", metavar="FILE", help="Analizuje plik .txt wyeksportowany z grupy WhatsApp")
    parser.add_argument("--country", choices=["BR", "MX"], default="BR", help="Kraj dla --import-whatsapp (domyślnie BR)")
    parser.add_argument("--test-gemini", action="store_true", help="Testuje połączenie z Gemini Interactions API")
    parser.add_argument("--stats", action="store_true", help="Wyświetla statystyki bazy leads.db")

    args = parser.parse_args()

    if args.stats:
        init_db()
        s = get_stats()
        print("\n📊 STATYSTYKI SERVICEAPP SOCIAL GROUPS BOT:")
        print(f"  • Łącznie leadów:   {s['total']}")
        print(f"  • 🟢 WhatsApp:      {s['whatsapp']}")
        print(f"  • 🔵 Facebook:      {s['facebook']}")
        print(f"  • 🎵 TikTok:        {s['tiktok']}")
        print(f"  • 🇧🇷 Brazylia:      {s['brazil']}")
        print(f"  • 🇲🇽 Meksyk:        {s['mexico']}")
        print(f"  • Wysłane alerty:   {s['notified']}")
        print(f"  • Google Play URL:  {GOOGLE_PLAY_URL}")
        return

    if args.test_gemini:
        client = GeminiClient()
        if not client.is_configured():
            print("[!] Brak GEMINI_API_KEY w .env / GitHub Secrets (utwórz darmowy klucz Free Tier: https://aistudio.google.com/apikey).")
            sys.exit(1)
        print(f"[*] Test Gemini Interactions API ({client.api_version}, model: {client.default_model})...")
        try:
            res = client.health_check()
            print(f"[✓] OK | status={res.status} | odpowiedź={res.output_text!r}")
        except GeminiAPIError as exc:
            print(f"[!] Błąd Gemini API: {exc}")
            sys.exit(1)
        return

    if args.import_whatsapp:
        init_db()
        analyzer = LeadAnalyzer()
        items = load_whatsapp_export_file(args.import_whatsapp, country=args.country)
        print(f"[*] Wczytano {len(items)} wiadomości z eksportu WhatsApp ({args.country})...")
        leads = process_items(items, analyzer, dry_run=args.dry_run)
        print(f"[✓] Znaleziono {len(leads)} leadów z eksportu WhatsApp.")
        return

    if args.webhook:
        init_db()
        analyzer = LeadAnalyzer()

        def handle_post(item: Dict[str, Any]) -> Dict[str, Any]:
            leads = process_items([item], analyzer, dry_run=args.dry_run)
            if leads:
                return {"lead_type": leads[0]["lead_type"], "ai_draft": leads[0]["ai_draft"]}
            return {"lead_type": "IRRELEVANT"}

        start_webhook_server(handle_post, port=args.port)
        return

    run_scan(mock=args.mock, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
