import re
from typing import Optional, Tuple

from config import (
    APP_NAME,
    APP_URL,
    APP_VALUE_PROPOSITION_BR_CLIENT,
    APP_VALUE_PROPOSITION_BR_WORKER,
    APP_VALUE_PROPOSITION_MX_CLIENT,
    APP_VALUE_PROPOSITION_MX_WORKER,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GOOGLE_PLAY_URL,
)
from gemini_client import GeminiAPIError, GeminiClient

LEAD_SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {"type": "string", "enum": ["SERVICE_SEEKER", "WORK_SEEKER", "IRRELEVANT"]},
        "draft_reply": {"type": "string"},
    },
    "required": ["intent", "draft_reply"],
}


class LeadAnalyzer:
    def __init__(self, api_key: str = GEMINI_API_KEY, model: str = GEMINI_MODEL):
        self.gemini = GeminiClient(api_key=api_key, default_model=model)

    def analyze(self, title: str, content: str, country: str = "BR", platform: str = "whatsapp") -> Tuple[str, Optional[str]]:
        combined = f"{title}\n{content}".lower()
        intent = self._classify_heuristic(combined, country)
        if intent == "IRRELEVANT":
            return "IRRELEVANT", None

        if self.gemini.is_configured():
            try:
                ai_res = self._analyze_with_gemini(title, content, country, platform)
                if ai_res:
                    return ai_res
            except (GeminiAPIError, ValueError, KeyError) as exc:
                print(f"[!] Gemini fallback ({exc}) -> używam szablonu regułowego.")

        return intent, self._draft_heuristic(intent, country)

    def _classify_heuristic(self, text: str, country: str) -> str:
        if country == "MX":
            service_patterns = [
                r"(busco|necesito) (un |una )?(buen |buena )?(plomero|electricista|albañil|pintor|técnico|tecnico|carpintero|cerrajero|herrero|jardinero|mec[aá]nico)",
                r"(recomienden|alguien recomienda|conocen a) (un |una )?(buen |buena )?(plomero|electricista|albañil|pintor|carpintero|cerrajero|técnico|tecnico|señora de limpieza)",
                r"cotizaci[oó]n para (remodelaci[oó]n|trabajo|reparaci[oó]n|pintura|plomer[ií]a|electricidad|obra)",
                r"necesito contratar (a alguien|un servicio)",
                r"busco (señora|persona|alguien) (de|para) limpieza",
            ]
            work_patterns = [
                r"(busco|necesito|me urge) (chamba|trabajo|empleo|jale)",
                r"hago trabajos de (albañiler[ií]a|plomer[ií]a|electricidad|pintura|carpinter[ií]a|mantenimiento)",
                r"ofrezco (mis )?servicios",
                r"d[oó]nde (conseguir clientes|anunciar mi trabajo|ofrecer mis servicios)",
                r"trabajador independiente",
                r"ingreso(s)? extra",
            ]
        else:
            service_patterns = [
                r"(preciso|procuro) (de )?(um |uma )?(bom |boa )?(encanador|eletricista|diarista|faxineira|pedreiro|pintor|marceneiro|chaveiro|jardineiro|técnico|tecnico|montador|profissional|marido de aluguel)",
                r"(alguém|alguem) (indica|recomenda|conhece|tem contato de?) (um |uma )?(bom |boa )?(encanador|eletricista|diarista|faxineira|pedreiro|pintor|marceneiro|chaveiro|técnico|tecnico|profissional)",
                r"indica[cç][aã]o de (um |uma )?(encanador|eletricista|diarista|pedreiro|pintor|profissional|faxineira|técnico|tecnico)",
                r"or[cç]amento para (reforma|pintura|obra|servi[cç]o|reparo|instala[cç][aã]o)",
                r"contratar (servi[cç]o|profissional|diarista|pedreiro|eletricista|encanador)",
            ]
            work_patterns = [
                r"como conseguir clientes",
                r"onde divulgar (meu trabalho|meus servi[cç]os)",
                r"trabalho aut[oô]nomo",
                r"(procurando|precisando de|buscando) (tramp[oa]|bico|renda extra|trabalho|emprego|servi[cç]o|freela)",
                r"fa[cç]o servi[cç]os de (el[eé]trica|hidr[aá]ulica|pintura|reforma|manuten[cç][aã]o|limpeza|marcenaria)",
                r"prestador de servi[cç]o",
            ]

        for pattern in service_patterns:
            if re.search(pattern, text):
                return "SERVICE_SEEKER"
        for pattern in work_patterns:
            if re.search(pattern, text):
                return "WORK_SEEKER"
        return "IRRELEVANT"

    def _draft_heuristic(self, lead_type: str, country: str) -> str:
        if country == "MX":
            if lead_type == "SERVICE_SEEKER":
                return (
                    f"¡Hola! Si todavía estás buscando, te recomiendo probar {APP_NAME} "
                    f"(Google Play: {GOOGLE_PLAY_URL} | Web: {APP_URL}). "
                    f"Es {APP_VALUE_PROPOSITION_MX_CLIENT}. "
                    "Puedes pedir cotizaciones gratis y comparar reseñas antes de contratar."
                )
            return (
                f"¡Qué tal colega! Para conseguir más chamba local, puedes registrarte en {APP_NAME} "
                f"(Google Play: {GOOGLE_PLAY_URL} | Web: {APP_URL}). "
                f"Es {APP_VALUE_PROPOSITION_MX_WORKER}. ¡Mucho éxito!"
            )

        if lead_type == "SERVICE_SEEKER":
            return (
                f"Olá! Se ainda estiver procurando, dá uma olhada no {APP_NAME} "
                f"(Google Play: {GOOGLE_PLAY_URL} | Site: {APP_URL}). "
                f"É {APP_VALUE_PROPOSITION_BR_CLIENT}. "
                "Dá para pedir orçamentos grátis e ver avaliações antes de fechar!"
            )
        return (
            f"Fala parceiro! Para conseguir mais clientes na sua região, vale testar o {APP_NAME} "
            f"(Google Play: {GOOGLE_PLAY_URL} | Site: {APP_URL}). "
            f"É {APP_VALUE_PROPOSITION_BR_WORKER}. Boa sorte!"
        )

    def _analyze_with_gemini(self, title: str, content: str, country: str, platform: str) -> Optional[Tuple[str, Optional[str]]]:
        country_name = "México" if country == "MX" else "Brasil"
        lang_hint = "Español de México (ES-MX)" if country == "MX" else "Português do Brasil (PT-BR)"
        system_instruction = (
            f"Você ajuda o aplicativo {APP_NAME} (Google Play: {GOOGLE_PLAY_URL}, Site: {APP_URL}) no {country_name}. "
            f"Analise a mensagem vinda de {platform} e classifique como SERVICE_SEEKER, WORK_SEEKER ou IRRELEVANT. "
            f"Se for relevante, escreva uma resposta curta (2-3 frases), natural e sem spam em {lang_hint}, "
            f"incluindo o link do Google Play: {GOOGLE_PLAY_URL}."
        )
        parsed, _ = self.gemini.create_structured_json(
            input_data=f"PLATAFORMA: {platform}\nPAÍS: {country_name}\nTÍTULO: {title}\nCONTEÚDO: {content}",
            schema=LEAD_SCHEMA,
            system_instruction=system_instruction,
        )
        if not isinstance(parsed, dict):
            return None
        intent = parsed.get("intent", "IRRELEVANT")
        if intent == "IRRELEVANT":
            return "IRRELEVANT", None
        if intent not in ("SERVICE_SEEKER", "WORK_SEEKER"):
            return None
        draft = (parsed.get("draft_reply") or "").strip()
        if GOOGLE_PLAY_URL not in draft:
            draft = f"{draft} (Google Play: {GOOGLE_PLAY_URL})".strip()
        return intent, draft
