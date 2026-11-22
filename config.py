import os

# ==============================================================================
# SERVICEAPP — SOCIAL GROUPS BOT (WhatsApp, TikTok, Facebook Groups — BR & MX)
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
APP_VALUE_PROPOSITION_MX_CLIENT = (
    "una app donde puedes encontrar y comparar cotizaciones de profesionales "
    "y trabajadores de oficio calificados en tu zona"
)
APP_VALUE_PROPOSITION_MX_WORKER = (
    "una app para trabajadores independientes, técnicos y especialistas para conseguir más clientes, "
    "recibir solicitudes de chamba y generar ingresos extra"
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
USER_AGENT = "ServiceAppSocialGroupsBot/1.0 (+https://serviceapp.mobi)"
DB_PATH = os.path.join(os.path.dirname(__file__), "leads.db")

# ==============================================================================
# PUBLICZNE ZAPYTANIA RSS (tylko publicznie indeksowane treści — 0 zł, bez omijania blokad)
# ==============================================================================
PUBLIC_RSS_QUERIES = [
    # Brazylia — Facebook Groups / Pages
    {
        "platform": "facebook",
        "country": "BR",
        "channel": "Facebook Grupos (BR)",
        "hl": "pt-BR",
        "gl": "BR",
        "ceid": "BR:pt-419",
        "query": 'site:facebook.com ("preciso de encanador" OR "preciso de eletricista" OR "indicação de diarista" OR "preciso de pedreiro" OR "orçamento reforma")',
    },
    # Brazylia — TikTok
    {
        "platform": "tiktok",
        "country": "BR",
        "channel": "TikTok (BR)",
        "hl": "pt-BR",
        "gl": "BR",
        "ceid": "BR:pt-419",
        "query": 'site:tiktok.com ("trabalho autônomo" OR "como conseguir clientes" OR "prestador de serviço" OR "encanador" OR "eletricista" OR "diarista") brasil',
    },
    # Brazylia — WhatsApp public group invites / local services
    {
        "platform": "whatsapp",
        "country": "BR",
        "channel": "WhatsApp Grupos (BR)",
        "hl": "pt-BR",
        "gl": "BR",
        "ceid": "BR:pt-419",
        "query": '("grupo whatsapp" OR site:chat.whatsapp.com) ("serviços" OR "trampo" OR "diarista" OR "pedreiro" OR "eletricista") brasil',
    },
    # Meksyk — Facebook Groups / Pages
    {
        "platform": "facebook",
        "country": "MX",
        "channel": "Facebook Grupos (MX)",
        "hl": "es-419",
        "gl": "MX",
        "ceid": "MX:es-419",
        "query": 'site:facebook.com ("busco plomero" OR "busco electricista" OR "busco albañil" OR "busco chamba" OR "ofrezco servicios") mexico',
    },
    # Meksyk — TikTok
    {
        "platform": "tiktok",
        "country": "MX",
        "channel": "TikTok (MX)",
        "hl": "es-419",
        "gl": "MX",
        "ceid": "MX:es-419",
        "query": 'site:tiktok.com ("busco chamba" OR "plomero" OR "electricista" OR "albañil" OR "trabajador independiente") mexico',
    },
    # Meksyk — WhatsApp public group mentions
    {
        "platform": "whatsapp",
        "country": "MX",
        "channel": "WhatsApp Grupos (MX)",
        "hl": "es-419",
        "gl": "MX",
        "ceid": "MX:es-419",
        "query": '("grupo whatsapp" OR site:chat.whatsapp.com) ("chamba" OR "plomero" OR "electricista" OR "oficios") mexico',
    },
]
