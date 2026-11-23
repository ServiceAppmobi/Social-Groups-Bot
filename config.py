import os

# ==============================================================================
# SERVICEAPP — SOCIAL GROUPS BOT (WhatsApp, TikTok, Facebook — 17 krajów)
# ==============================================================================
APP_NAME = os.getenv("APP_NAME") or "ServiceApp"
APP_URL = os.getenv("APP_URL") or "https://serviceapp.mobi"
GOOGLE_PLAY_URL = (
    os.getenv("GOOGLE_PLAY_URL")
    or "https://play.google.com/store/apps/details?id=pl.serviceapp&pli=1"
)

APP_VALUE_PROPOSITION_BR_CLIENT = (
    "um aplicativo onde você encontra e compara orçamentos de profissionais autônomos "
    "e prestadores de serviços avaliados na sua região"
)
APP_VALUE_PROPOSITION_BR_WORKER = (
    "um aplicativo gratuito para autônomos e prestadores de serviços conseguirem clientes locais, "
    "receberem pedidos de orçamento e aumentarem a renda"
)
APP_VALUE_PROPOSITION_ES_CLIENT = (
    "una app donde puedes encontrar y comparar cotizaciones de profesionales "
    "y trabajadores de oficio calificados en tu zona"
)
APP_VALUE_PROPOSITION_ES_WORKER = (
    "una app para trabajadores independientes, técnicos y especialistas para conseguir más clientes, "
    "recibir solicitudes de trabajo y generar ingresos extra"
)
APP_VALUE_PROPOSITION_EN_CLIENT = (
    "a local services app where you can request free quotes and compare rated plumbers, "
    "electricians, cleaners, and handymen near you"
)
APP_VALUE_PROPOSITION_EN_WORKER = (
    "a mobile app connecting independent tradespeople, technicians, and freelancers "
    "directly with local customers looking for services"
)
APP_VALUE_PROPOSITION_FR_CLIENT = (
    "une application locale pour demander des devis gratuits et comparer des artisans "
    "et professionnels évalués près de chez vous"
)
APP_VALUE_PROPOSITION_FR_WORKER = (
    "une application qui connecte les travailleurs autonomes et artisans "
    "avec des clients locaux qui recherchent des services"
)
APP_VALUE_PROPOSITION_JA_CLIENT = (
    "お近くの信頼できる水道・電気・清掃・リフォーム業者を比較し、無料で見積もり依頼できるアプリ"
)
APP_VALUE_PROPOSITION_JA_WORKER = (
    "地元の顧客から直接仕事や見積もり依頼を受け取れる、個人事業主・技術者向けのマッチングアプリ"
)

# ==============================================================================
# POWIADOMIENIA (Resend / Telegram / ntfy)
# ==============================================================================
RESEND_API_KEY = os.getenv("RESEND_API_KEY") or ""
EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT") or "karolak.pawel@gmail.com"
EMAIL_SENDER = os.getenv("EMAIL_SENDER") or "onboarding@resend.dev"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or ""
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or ""
NTFY_TOPIC = os.getenv("NTFY_TOPIC") or ""
NTFY_SERVER = os.getenv("NTFY_SERVER") or "https://ntfy.sh"

# ==============================================================================
# AI / GEMINI INTERACTIONS API (Opcjonalne — Free Tier friendly)
# ==============================================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or ""
GEMINI_MODEL = os.getenv("GEMINI_MODEL") or "gemini-3.5-flash-lite"
GEMINI_API_VERSION = os.getenv("GEMINI_API_VERSION") or "v1"
GEMINI_TIMEOUT_SECONDS = int(os.getenv("GEMINI_TIMEOUT_SECONDS") or "30")

# ==============================================================================
# WEBHOOK & HARMONOGRAM
# ==============================================================================
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT") or "8089")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET") or ""
MAX_POST_AGE_DAYS = int(os.getenv("MAX_POST_AGE_DAYS") or "30")
USER_AGENT = "ServiceAppSocialGroupsBot/1.2 (+https://serviceapp.mobi)"
DB_PATH = os.path.join(os.path.dirname(__file__), "leads.db")

# Domyślnie: wszystkie pozostałe radary wstrzymane (on hold), aktywny wyłącznie fokus na São Paulo.
# Aby wznowić wszystkie 17 krajów: ACTIVE_COUNTRIES=ALL oraz CITY_FILTER=
ACTIVE_COUNTRIES_RAW = (os.getenv("ACTIVE_COUNTRIES") or "BR").strip()
CITY_FILTER = (os.getenv("CITY_FILTER") if os.getenv("CITY_FILTER") is not None else "São Paulo").strip()
SAO_PAULO_TERMS = (
    "são paulo",
    "sao paulo",
    "sampa",
    "grande sp",
    "capital sp",
    "zona sul",
    "zona leste",
    "zona norte",
    "zona oeste",
    "vila mariana",
    "pinheiros",
    "moema",
    "itaim",
    "tatuapé",
    "tatuape",
    "itaquera",
    "santana",
    "lapa",
    "morumbi",
    "perdizes",
    "paulista",
    "osasco",
    "guarulhos",
    "santo andré",
    "santo andre",
    "são bernardo",
    "sao bernardo",
    "abc paulista",
)

COUNTRIES = {
    # --- South America (All 12) ---
    "BR": {"name": "Brazylia", "flag": "🇧🇷", "lang": "pt", "lang_label": "PT-BR", "hl": "pt-BR", "gl": "BR", "ceid": "BR:pt-419"},
    "AR": {"name": "Argentyna", "flag": "🇦🇷", "lang": "es", "lang_label": "ES-AR", "hl": "es-419", "gl": "AR", "ceid": "AR:es-419"},
    "CO": {"name": "Kolumbia", "flag": "🇨🇴", "lang": "es", "lang_label": "ES-CO", "hl": "es-419", "gl": "CO", "ceid": "CO:es-419"},
    "CL": {"name": "Chile", "flag": "🇨🇱", "lang": "es", "lang_label": "ES-CL", "hl": "es-419", "gl": "CL", "ceid": "CL:es-419"},
    "PE": {"name": "Peru", "flag": "🇵🇪", "lang": "es", "lang_label": "ES-PE", "hl": "es-419", "gl": "PE", "ceid": "PE:es-419"},
    "EC": {"name": "Ekwador", "flag": "🇪🇨", "lang": "es", "lang_label": "ES-EC", "hl": "es-419", "gl": "EC", "ceid": "EC:es-419"},
    "VE": {"name": "Wenezuela", "flag": "🇻🇪", "lang": "es", "lang_label": "ES-VE", "hl": "es-419", "gl": "VE", "ceid": "VE:es-419"},
    "UY": {"name": "Urugwaj", "flag": "🇺🇾", "lang": "es", "lang_label": "ES-UY", "hl": "es-419", "gl": "UY", "ceid": "UY:es-419"},
    "PY": {"name": "Paragwaj", "flag": "🇵🇾", "lang": "es", "lang_label": "ES-PY", "hl": "es-419", "gl": "PY", "ceid": "PY:es-419"},
    "BO": {"name": "Boliwia", "flag": "🇧🇴", "lang": "es", "lang_label": "ES-BO", "hl": "es-419", "gl": "BO", "ceid": "BO:es-419"},
    "GY": {"name": "Gujana", "flag": "🇬🇾", "lang": "en", "lang_label": "EN-GY", "hl": "en", "gl": "GY", "ceid": "GY:en"},
    "SR": {"name": "Surinam", "flag": "🇸🇷", "lang": "nl", "lang_label": "NL/EN-SR", "hl": "nl", "gl": "SR", "ceid": "SR:nl"},
    # --- North America ---
    "MX": {"name": "Meksyk", "flag": "🇲🇽", "lang": "es", "lang_label": "ES-MX", "hl": "es-419", "gl": "MX", "ceid": "MX:es-419"},
    "US": {"name": "USA", "flag": "🇺🇸", "lang": "en", "lang_label": "EN-US", "hl": "en-US", "gl": "US", "ceid": "US:en"},
    "CA": {"name": "Kanada", "flag": "🇨🇦", "lang": "en", "lang_label": "EN/FR-CA", "hl": "en-CA", "gl": "CA", "ceid": "CA:en"},
    # --- Asia ---
    "SG": {"name": "Singapur", "flag": "🇸🇬", "lang": "en", "lang_label": "EN-SG", "hl": "en-SG", "gl": "SG", "ceid": "SG:en"},
    "JP": {"name": "Japonia", "flag": "🇯🇵", "lang": "ja", "lang_label": "JA/EN-JP", "hl": "ja", "gl": "JP", "ceid": "JP:ja"},
}


def get_country_info(code: str) -> dict:
    c = (code or "BR").upper()
    return COUNTRIES.get(c, {"name": c, "flag": "🌎", "lang": "en", "lang_label": "EN", "hl": "en-US", "gl": "US", "ceid": "US:en"})


def _build_public_rss_queries():
    queries = []
    # Brazylia (PT-BR)
    queries.extend([
        {"platform": "facebook", "country": "BR", "channel": "Facebook Grupos (BR)", "hl": "pt-BR", "gl": "BR", "ceid": "BR:pt-419", "query": 'site:facebook.com ("preciso de encanador" OR "preciso de eletricista" OR "indicação de diarista" OR "orçamento reforma")'},
        {"platform": "tiktok", "country": "BR", "channel": "TikTok (BR)", "hl": "pt-BR", "gl": "BR", "ceid": "BR:pt-419", "query": 'site:tiktok.com ("trabalho autônomo" OR "como conseguir clientes" OR "encanador" OR "eletricista" OR "diarista") brasil'},
        {"platform": "whatsapp", "country": "BR", "channel": "WhatsApp Grupos (BR)", "hl": "pt-BR", "gl": "BR", "ceid": "BR:pt-419", "query": '("grupo whatsapp" OR site:chat.whatsapp.com) ("serviços" OR "trampo" OR "diarista" OR "eletricista") brasil'},
    ])
    # Meksyk + hiszpańskojęzyczna Ameryka Południowa (MX, AR, CO, CL, PE, EC, VE, UY, PY, BO)
    es_countries = [
        ("MX", "mexico"),
        ("AR", "argentina"),
        ("CO", "colombia"),
        ("CL", "chile"),
        ("PE", "peru"),
        ("EC", "ecuador"),
        ("VE", "venezuela"),
        ("UY", "uruguay"),
        ("PY", "paraguay"),
        ("BO", "bolivia"),
    ]
    for code, kw_country in es_countries:
        c = COUNTRIES[code]
        queries.append({
            "platform": "facebook",
            "country": code,
            "channel": f"Facebook Grupos ({code})",
            "hl": c["hl"], "gl": c["gl"], "ceid": c["ceid"],
            "query": f'site:facebook.com ("busco plomero" OR "busco electricista" OR "busco gasfitero" OR "busco albañil" OR "busco trabajo" OR "ofrezco servicios") {kw_country}',
        })
        queries.append({
            "platform": "tiktok",
            "country": code,
            "channel": f"TikTok ({code})",
            "hl": c["hl"], "gl": c["gl"], "ceid": c["ceid"],
            "query": f'site:tiktok.com ("plomero" OR "electricista" OR "albañil" OR "chamba" OR "laburo" OR "oficios") {kw_country}',
        })
    queries.append({
        "platform": "whatsapp",
        "country": "MX",
        "channel": "WhatsApp Grupos (LatAm ES)",
        "hl": "es-419", "gl": "MX", "ceid": "MX:es-419",
        "query": '("grupo whatsapp" OR site:chat.whatsapp.com) ("chamba" OR "laburo" OR "plomero" OR "electricista" OR "oficios")',
    })
    # Gujana & Surinam (South America EN/NL)
    queries.append({
        "platform": "facebook", "country": "GY", "channel": "Facebook Groups (GY)",
        "hl": "en", "gl": "GY", "ceid": "GY:en",
        "query": 'site:facebook.com ("plumber" OR "electrician" OR "handyman" OR "cleaner") guyana',
    })
    queries.append({
        "platform": "facebook", "country": "SR", "channel": "Facebook Groepen (SR)",
        "hl": "nl", "gl": "SR", "ceid": "SR:nl",
        "query": 'site:facebook.com ("loodgieter" OR "elektricien" OR "klusjesman" OR "handyman") suriname',
    })
    # USA, Kanada, Singapur (EN / FR)
    en_targets = [
        ("US", "USA", "united states"),
        ("CA", "Canada", "canada"),
        ("SG", "Singapore", "singapore"),
    ]
    for code, label, kw_country in en_targets:
        c = COUNTRIES[code]
        extra = ' OR "aircon servicing"' if code == "SG" else ' OR "plombier"' if code == "CA" else ""
        queries.append({
            "platform": "facebook", "country": code, "channel": f"Facebook Groups ({label})",
            "hl": c["hl"], "gl": c["gl"], "ceid": c["ceid"],
            "query": f'site:facebook.com ("need a plumber" OR "looking for a handyman" OR "recommend an electrician" OR "house cleaner"{extra}) {kw_country}',
        })
        queries.append({
            "platform": "tiktok", "country": code, "channel": f"TikTok ({label})",
            "hl": c["hl"], "gl": c["gl"], "ceid": c["ceid"],
            "query": f'site:tiktok.com ("handyman business" OR "how to get clients" OR "plumber" OR "electrician"{extra}) {kw_country}',
        })
        queries.append({
            "platform": "whatsapp", "country": code, "channel": f"WhatsApp Groups ({label})",
            "hl": c["hl"], "gl": c["gl"], "ceid": c["ceid"],
            "query": f'("whatsapp group" OR site:chat.whatsapp.com) ("handyman" OR "plumber" OR "services" OR "jobs") {kw_country}',
        })
    # Japonia (JA + EN)
    queries.extend([
        {
            "platform": "facebook", "country": "JP", "channel": "Facebook Groups (JP)",
            "hl": "ja", "gl": "JP", "ceid": "JP:ja",
            "query": 'site:facebook.com ("水道修理" OR "電気工事" OR "ハウスクリーニング" OR "便利屋" OR "handyman tokyo" OR "plumber japan")',
        },
        {
            "platform": "tiktok", "country": "JP", "channel": "TikTok (JP)",
            "hl": "ja", "gl": "JP", "ceid": "JP:ja",
            "query": 'site:tiktok.com ("便利屋" OR "ハウスクリーニング" OR "電気工事" OR "水道修理" OR "副業 仕事探し")',
        },
        {
            "platform": "whatsapp", "country": "JP", "channel": "WhatsApp Groups (JP)",
            "hl": "en", "gl": "JP", "ceid": "JP:en",
            "query": '("whatsapp group" OR site:chat.whatsapp.com) ("tokyo" OR "osaka" OR "japan") ("handyman" OR "moving" OR "cleaning" OR "jobs")',
        },
    ])
    return queries


PUBLIC_RSS_QUERIES = _build_public_rss_queries()

SAO_PAULO_RSS_QUERIES = [
    {
        "platform": "facebook",
        "country": "BR",
        "channel": "Facebook Grupos (São Paulo)",
        "hl": "pt-BR",
        "gl": "BR",
        "ceid": "BR:pt-419",
        "query": 'site:facebook.com ("São Paulo" OR "Zona Sul" OR "Zona Leste" OR "Zona Norte" OR "Zona Oeste") ("preciso de encanador" OR "preciso de eletricista" OR "indicação de diarista" OR "preciso de pedreiro" OR "orçamento reforma")',
    },
    {
        "platform": "tiktok",
        "country": "BR",
        "channel": "TikTok (São Paulo)",
        "hl": "pt-BR",
        "gl": "BR",
        "ceid": "BR:pt-419",
        "query": 'site:tiktok.com ("São Paulo" OR "SP") ("trabalho autônomo" OR "como conseguir clientes" OR "encanador" OR "eletricista" OR "diarista" OR "pedreiro")',
    },
    {
        "platform": "whatsapp",
        "country": "BR",
        "channel": "WhatsApp Grupos (São Paulo)",
        "hl": "pt-BR",
        "gl": "BR",
        "ceid": "BR:pt-419",
        "query": '("grupo whatsapp" OR site:chat.whatsapp.com) ("São Paulo" OR "SP") ("serviços" OR "trampo" OR "diarista" OR "eletricista" OR "encanador")',
    },
]


def get_active_rss_queries():
    """Zwraca aktywne zapytania RSS (domyślnie TYLKO São Paulo; ACTIVE_COUNTRIES=ALL & CITY_FILTER= włącza 17 krajów)."""
    if CITY_FILTER.lower() in ("são paulo", "sao paulo", "sp") and ACTIVE_COUNTRIES_RAW.upper() != "ALL":
        return list(SAO_PAULO_RSS_QUERIES)
    if ACTIVE_COUNTRIES_RAW.upper() == "ALL":
        return list(PUBLIC_RSS_QUERIES)
    allowed = {c.strip().upper() for c in ACTIVE_COUNTRIES_RAW.split(",") if c.strip()}
    return [q for q in PUBLIC_RSS_QUERIES if q["country"] in allowed]


def matches_city_filter(title: str, content: str, source_channel: str = "", city_filter: str = CITY_FILTER) -> bool:
    if not city_filter:
        return True
    haystack = f"{source_channel} {title} {content}".lower()
    cf = city_filter.lower()
    if cf in ("são paulo", "sao paulo", "sp"):
        return any(term in haystack for term in SAO_PAULO_TERMS)
    return cf in haystack
