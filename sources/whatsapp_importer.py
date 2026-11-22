import hashlib
import os
import re
import time
from typing import Any, Dict, List

# Obsługuje eksporty czatów WhatsApp (Android i iOS, formaty BR/MX/EU):
# np. "22/11/2026 14:35 - Maria: Preciso de encanador..."
# lub "[22/11/2026, 14:35:10] Juan: Busco plomero..."
WHATSAPP_LINE_RE = re.compile(
    r"^\[?(\d{1,2}/\d{1,2}/\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s?[APMapm\.]{2,4})?)\]?\s*(?:-|\u2013)?\s*([^:]{1,80}):\s+(.+)$"
)


def parse_whatsapp_export_text(
    raw_text: str,
    group_name: str = "WhatsApp Export",
    country: str = "BR",
) -> List[Dict[str, Any]]:
    """Parsuje plik .txt wyeksportowany z grupy WhatsApp na listę wiadomości."""
    messages: List[Dict[str, Any]] = []
    current: Dict[str, Any] = {}

    for line in (raw_text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        match = WHATSAPP_LINE_RE.match(line)
        if match:
            if current:
                messages.append(current)
            date_str, time_str, sender, body = match.groups()
            digest = hashlib.sha256(f"{group_name}:{date_str}:{time_str}:{sender}:{body}".encode("utf-8")).hexdigest()[:16]
            current = {
                "id": f"whatsapp_export_{digest}",
                "platform": "whatsapp",
                "country": country,
                "source_channel": f"WhatsApp Grupo: {group_name}",
                "title": body[:90] + ("..." if len(body) > 90 else ""),
                "content": body,
                "url": "https://web.whatsapp.com",
                "author": sender.strip(),
                "created_utc": time.time(),
            }
        elif current:
            current["content"] = f"{current['content']} {line}".strip()[:1500]

    if current:
        messages.append(current)

    return messages


def load_whatsapp_export_file(filepath: str, country: str = "BR") -> List[Dict[str, Any]]:
    group_name = os.path.splitext(os.path.basename(filepath))[0]
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        return parse_whatsapp_export_text(f.read(), group_name=group_name, country=country)
