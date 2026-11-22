import hashlib
import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Callable, Dict, Optional

from config import COUNTRIES, WEBHOOK_PORT, WEBHOOK_SECRET

PHONE_PREFIX_TO_COUNTRY = [
    ("593", "EC"), ("598", "UY"), ("595", "PY"), ("591", "BO"), ("592", "GY"), ("597", "SR"),
    ("55", "BR"), ("52", "MX"), ("54", "AR"), ("57", "CO"), ("56", "CL"), ("51", "PE"),
    ("58", "VE"), ("65", "SG"), ("81", "JP"),
]


def _detect_country(sender_phone: str, channel: str, body: str) -> str:
    digits = "".join(ch for ch in sender_phone if ch.isdigit())
    for prefix, code in PHONE_PREFIX_TO_COUNTRY:
        if digits.startswith(prefix):
            return code
    hint = f"{channel} {body}".lower()
    if any(w in hint for w in ("singapore", "aircon", "hdb")):
        return "SG"
    if any(w in hint for w in ("tokyo", "osaka", "japan", "水道", "電気工事", "便利屋", "ハウスクリーニング")):
        return "JP"
    if any(w in hint for w in ("canada", "toronto", "vancouver", "montreal", "quebec", "calgary", "plombier")):
        return "CA"
    if any(w in hint for w in ("usa", "new york", "texas", "california", "florida", "chicago", "handyman")):
        return "US"
    if any(w in hint for w in ("argentina", "buenos aires", "cordoba", "laburo")):
        return "AR"
    if any(w in hint for w in ("colombia", "bogota", "medellin", "camello")):
        return "CO"
    if any(w in hint for w in ("chile", "santiago", "gasfiter")):
        return "CL"
    if any(w in hint for w in ("peru", "lima")):
        return "PE"
    if any(w in hint for w in ("ecuador", "quito", "guayaquil")):
        return "EC"
    if any(w in hint for w in ("venezuela", "caracas")):
        return "VE"
    if any(w in hint for w in ("uruguay", "montevideo")):
        return "UY"
    if any(w in hint for w in ("paraguay", "asuncion")):
        return "PY"
    if any(w in hint for w in ("bolivia", "la paz", "santa cruz")):
        return "BO"
    if "guyana" in hint:
        return "GY"
    if "suriname" in hint:
        return "SR"
    if any(w in hint for w in ("mexico", "méxico", "cdmx", "monterrey", "guadalajara", "chamba", "plomero")):
        return "MX"
    if digits.startswith("1"):
        return "US"
    return "BR"


def normalize_webhook_payload(platform: str, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Ujednolica webhook z WhatsApp (Evolution/Baileys/WPPConnect), Facebooka lub TikToka (Make/n8n/API)."""
    body = (
        (data.get("message") or {}).get("conversation")
        if isinstance(data.get("message"), dict)
        else None
    ) or data.get("body") or data.get("text") or data.get("content") or data.get("comment") or ""
    body = str(body).strip()
    if not body:
        return None

    title = str(data.get("title") or body[:90]).strip()
    channel = (
        data.get("groupName")
        or data.get("chatName")
        or data.get("channel")
        or data.get("source_channel")
        or f"{platform.capitalize()} Group"
    )
    author = data.get("pushName") or data.get("senderName") or data.get("author") or "usuario"
    sender_phone = str(data.get("sender") or data.get("phone") or "")
    country = (data.get("country") or "").upper()
    if country not in COUNTRIES:
        country = _detect_country(sender_phone, str(channel), body)

    raw_id = str(data.get("id") or "")
    if not raw_id:
        raw_id = hashlib.sha256(f"{platform}:{channel}:{author}:{body}".encode("utf-8")).hexdigest()[:16]

    default_url = (
        f"https://wa.me/{sender_phone}"
        if platform == "whatsapp" and sender_phone
        else f"https://www.{platform}.com"
    )
    url = str(data.get("url") or default_url)

    return {
        "id": f"{platform}_{raw_id}",
        "platform": platform,
        "country": country,
        "source_channel": str(channel),
        "title": title,
        "content": body[:1500],
        "url": url,
        "author": str(author),
        "created_utc": time.time(),
    }


class SocialWebhookHandler(BaseHTTPRequestHandler):
    on_post: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None
    dashboard_path: str = ""

    def _send_json(self, status: int, payload: Dict[str, Any]):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/dashboard"):
            if self.dashboard_path and os.path.exists(self.dashboard_path):
                with open(self.dashboard_path, "rb") as f:
                    content = f.read()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
        if self.path == "/health":
            self._send_json(200, {"ok": True, "service": "serviceapp-social-groups-bot"})
            return
        self._send_json(404, {"error": "Not found"})

    def do_POST(self):
        if WEBHOOK_SECRET:
            provided = self.headers.get("X-Webhook-Secret") or ""
            if provided != WEBHOOK_SECRET:
                self._send_json(401, {"error": "Unauthorized"})
                return

        route_map = {
            "/webhook/whatsapp": "whatsapp",
            "/webhook/facebook": "facebook",
            "/webhook/tiktok": "tiktok",
            "/webhook/social": "social",
        }
        platform = route_map.get(self.path.split("?")[0])
        if not platform:
            self._send_json(404, {"error": "Unknown webhook route"})
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            self._send_json(400, {"error": "Invalid JSON"})
            return

        if platform == "social":
            platform = str(payload.get("platform") or "whatsapp").lower()
            if platform not in ("whatsapp", "facebook", "tiktok"):
                platform = "whatsapp"

        item = normalize_webhook_payload(platform, payload)
        if not item:
            self._send_json(200, {"status": "ignored", "reason": "empty_body"})
            return

        result = self.on_post(item) if self.on_post else {"lead_type": "IRRELEVANT"}
        self._send_json(200, {"status": "processed", "id": item["id"], **result})


def start_webhook_server(on_post: Callable[[Dict[str, Any]], Dict[str, Any]], port: int = WEBHOOK_PORT):
    SocialWebhookHandler.on_post = on_post
    SocialWebhookHandler.dashboard_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard.html")
    server = HTTPServer(("", port), SocialWebhookHandler)
    print(f"[🚀] ServiceApp Social Groups Bot aktywny na http://localhost:{port}")
    print(f"     • Panel 1-klik (Facebook / TikTok / WhatsApp): http://localhost:{port}/dashboard")
    print(f"     • Webhook WhatsApp: POST http://localhost:{port}/webhook/whatsapp")
    print(f"     • Webhook Facebook: POST http://localhost:{port}/webhook/facebook")
    print(f"     • Webhook TikTok:   POST http://localhost:{port}/webhook/tiktok")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Zatrzymano serwer webhooków.")
        server.server_close()
