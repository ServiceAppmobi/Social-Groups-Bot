import email.utils
import hashlib
import html
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any, Dict, List

from config import CITY_FILTER, MAX_POST_AGE_DAYS, USER_AGENT, get_active_rss_queries, matches_city_filter


def _clean_html(raw: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


class PublicSocialRSSMonitor:
    """
    Skanuje wyłącznie publicznie indeksowane wzmianki z Facebooka, TikToka i WhatsAppa
    poprzez publiczne kanały RSS (zero logowania, zero omijania zabezpieczeń, 0 zł na GitHub Actions).
    """

    def __init__(self, max_age_days: int = MAX_POST_AGE_DAYS):
        self.max_age_days = max_age_days

    def fetch_query(self, cfg: Dict[str, str], limit: int = 25) -> List[Dict[str, Any]]:
        encoded = urllib.parse.quote(cfg["query"])
        url = (
            f"https://news.google.com/rss/search?q={encoded}"
            f"&hl={cfg['hl']}&gl={cfg['gl']}&ceid={cfg['ceid']}"
        )
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        results: List[Dict[str, Any]] = []
        cutoff = time.time() - (self.max_age_days * 86400) if self.max_age_days > 0 else 0

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status != 200:
                    return []
                root = ET.fromstring(resp.read())
                for item in root.findall(".//item")[:limit]:
                    title = _clean_html(item.findtext("title", default=""))
                    link = (item.findtext("link", default="") or "").strip()
                    desc = _clean_html(item.findtext("description", default=""))
                    pub_date = item.findtext("pubDate", default="")
                    created_utc = 0.0
                    if pub_date:
                        try:
                            created_utc = email.utils.parsedate_to_datetime(pub_date).timestamp()
                        except Exception:
                            created_utc = 0.0

                    if cutoff and created_utc and created_utc < cutoff:
                        continue
                    if not title or not link:
                        continue

                    digest = hashlib.sha256(f"{cfg['platform']}:{link}".encode("utf-8")).hexdigest()[:16]
                    results.append(
                        {
                            "id": f"{cfg['platform']}_rss_{digest}",
                            "platform": cfg["platform"],
                            "country": cfg["country"],
                            "source_channel": cfg["channel"],
                            "title": title,
                            "content": desc[:1000],
                            "url": link,
                            "author": cfg["channel"],
                            "created_utc": created_utc or time.time(),
                        }
                    )
        except Exception as exc:
            print(f"[!] Public RSS błąd ({cfg['channel']}): {exc}")
        return results

    def scan_all(self, limit_per_query: int = 25) -> List[Dict[str, Any]]:
        all_posts: List[Dict[str, Any]] = []
        active_queries = get_active_rss_queries()
        if CITY_FILTER:
            print(f"    [Aktywny filtr miasta: {CITY_FILTER} | pozostałe radary: ON HOLD]")
        for cfg in active_queries:
            posts = self.fetch_query(cfg, limit=limit_per_query)
            if CITY_FILTER:
                posts = [
                    p for p in posts
                    if matches_city_filter(p.get("title", ""), p.get("content", ""), p.get("source_channel", ""))
                ]
            print(f"    -> [{cfg['country']}] {cfg['channel']}: pobrano {len(posts)} pasujących wpisów")
            all_posts.extend(posts)
            time.sleep(0.3)

        unique = {p["id"]: p for p in all_posts}.values()
        return list(unique)

    @staticmethod
    def get_mock_posts() -> List[Dict[str, Any]]:
        now = time.time()
        return [
            {
                "id": "mock_wpp_br_01",
                "platform": "whatsapp",
                "country": "BR",
                "source_channel": "WhatsApp Grupo: [SP] Serviços e Reformas Zona Sul",
                "title": "Preciso de encanador urgente na Vila Mariana",
                "content": "Oi pessoal do grupo! Estou com vazamento no chuveiro e preciso de encanador de confiança hoje na Zona Sul de SP.",
                "url": "https://chat.whatsapp.com/mock-sp-servicos",
                "author": "Camila Souza (+55 11 99999-1111)",
                "created_utc": now - 900,
            },
            {
                "id": "mock_fb_br_01",
                "platform": "facebook",
                "country": "BR",
                "source_channel": "Facebook Grupo: Diaristas e Serviços Residenciais RJ",
                "title": "Alguém indica diarista ou eletricista no Méier?",
                "content": "Boa tarde grupo, preciso de indicação de eletricista e orçamento para reforma pequena no apartamento.",
                "url": "https://www.facebook.com/groups/mock-rj-servicos/posts/101",
                "author": "Rafael Lima",
                "created_utc": now - 1800,
            },
            {
                "id": "mock_tt_br_01",
                "platform": "tiktok",
                "country": "BR",
                "source_channel": "TikTok #trabalhoautonomo",
                "title": "Onde divulgar meu trabalho de pintura e elétrica?",
                "content": "Faço serviços de elétrica e pintura em Curitiba, estou procurando mais clientes e trabalho autônomo.",
                "url": "https://www.tiktok.com/@eletricista_curitiba/video/7000001",
                "author": "@eletricista_curitiba",
                "created_utc": now - 2400,
            },
            {
                "id": "mock_wpp_mx_01",
                "platform": "whatsapp",
                "country": "MX",
                "source_channel": "WhatsApp Grupo: Chamba y Oficios CDMX",
                "title": "Busco plomero urgente en Narvarte",
                "content": "Hola vecinos, busco un buen plomero para reparar una fuga en la cocina hoy mismo en CDMX.",
                "url": "https://chat.whatsapp.com/mock-cdmx-oficios",
                "author": "Luis Hernández (+52 55 1111-2222)",
                "created_utc": now - 1200,
            },
            {
                "id": "mock_fb_mx_01",
                "platform": "facebook",
                "country": "MX",
                "source_channel": "Facebook Grupo: Recomienden Servicios Monterrey",
                "title": "¿Alguien recomienda un albañil o pintor en San Nicolás?",
                "content": "Necesito cotización para remodelación de baño y pintura exterior en Monterrey.",
                "url": "https://www.facebook.com/groups/mock-mty-servicios/posts/202",
                "author": "Mariana Garza",
                "created_utc": now - 3000,
            },
            {
                "id": "mock_tt_mx_01",
                "platform": "tiktok",
                "country": "MX",
                "source_channel": "TikTok #chambamexico",
                "title": "Ofrezco mis servicios de plomería y electricidad en Guadalajara",
                "content": "Soy trabajador independiente, hago trabajos de plomería y electricidad en ZMG. Me urge chamba esta semana!",
                "url": "https://www.tiktok.com/@plomero_gdl/video/7000002",
                "author": "@plomero_gdl",
                "created_utc": now - 3600,
            },
        ]
