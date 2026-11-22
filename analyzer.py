import re
from typing import Optional, Tuple

from config import (
    APP_NAME,
    APP_URL,
    APP_VALUE_PROPOSITION_BR_CLIENT,
    APP_VALUE_PROPOSITION_BR_WORKER,
    APP_VALUE_PROPOSITION_EN_CLIENT,
    APP_VALUE_PROPOSITION_EN_WORKER,
    APP_VALUE_PROPOSITION_ES_CLIENT,
    APP_VALUE_PROPOSITION_ES_WORKER,
    APP_VALUE_PROPOSITION_FR_CLIENT,
    APP_VALUE_PROPOSITION_FR_WORKER,
    APP_VALUE_PROPOSITION_JA_CLIENT,
    APP_VALUE_PROPOSITION_JA_WORKER,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    GOOGLE_PLAY_URL,
    get_country_info,
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

JAPANESE_CHAR_RE = re.compile(r"[\u3040-\u30ff\u4e00-\u9faf]")
FRENCH_HINT_RE = re.compile(r"\b(plombier|[eé]lectricien|devis|r[eé]novation|cherche un|besoin d'un|travail autonome)\b")


class LeadAnalyzer:
    def __init__(self, api_key: str = GEMINI_API_KEY, model: str = GEMINI_MODEL):
        self.gemini = GeminiClient(api_key=api_key, default_model=model)

    def analyze(self, title: str, content: str, country: str = "BR", platform: str = "whatsapp") -> Tuple[str, Optional[str]]:
        combined = f"{title}\n{content}".lower()
        info = get_country_info(country)
        lang = info["lang"]
        intent = self._classify_heuristic(combined, country, lang)
        if intent == "IRRELEVANT":
            return "IRRELEVANT", None

        if self.gemini.is_configured():
            try:
                ai_res = self._analyze_with_gemini(title, content, country, platform)
                if ai_res:
                    return ai_res
            except (GeminiAPIError, ValueError, KeyError) as exc:
                print(f"[!] Gemini fallback ({exc}) -> używam szablonu regułowego.")

        reply_lang = self._detect_reply_language(combined, lang)
        return intent, self._draft_heuristic(intent, reply_lang)

    def _detect_reply_language(self, text: str, default_lang: str) -> str:
        if default_lang == "ja":
            return "ja" if JAPANESE_CHAR_RE.search(text) else "en"
        if default_lang == "en" and FRENCH_HINT_RE.search(text):
            return "fr"
        if default_lang == "nl":
            return "en"
        return default_lang

    def _classify_heuristic(self, text: str, country: str, lang: str = "pt") -> str:
        if lang == "pt":
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
        elif lang == "es":
            service_patterns = [
                r"(busco|necesito) (un |una )?(buen |buena )?(plomero|gasfitero|gasfiter|gasista|electricista|albañil|maestro|pintor|técnico|tecnico|carpintero|cerrajero|herrero|jardinero|mec[aá]nico)",
                r"(recomienden|recomiendan|alguien recomienda|conocen a) (un |una )?(buen |buena )?(plomero|gasfitero|gasfiter|gasista|electricista|albañil|pintor|carpintero|cerrajero|técnico|tecnico|señora de limpieza)",
                r"(cotizaci[oó]n|presupuesto) para (remodelaci[oó]n|trabajo|reparaci[oó]n|pintura|plomer[ií]a|electricidad|obra)",
                r"necesito contratar (a alguien|un servicio)",
                r"busco (señora|persona|alguien) (de|para) limpieza",
            ]
            work_patterns = [
                r"(busco|necesito|me urge) (chamba|laburo|pega|camello|trabajo|empleo|jale)",
                r"hago trabajos de (albañiler[ií]a|plomer[ií]a|gasfiter[ií]a|electricidad|pintura|carpinter[ií]a|mantenimiento)",
                r"ofrezco (mis )?servicios",
                r"d[oó]nde (conseguir clientes|anunciar mi trabajo|ofrecer mis servicios)",
                r"trabajador independiente",
                r"ingreso(s)? extra",
            ]
        elif lang == "ja":
            service_patterns = [
                r"(水道修理|電気工事|ハウスクリーニング|エアコン掃除|エアコン修理|リフォーム|便利屋|鍵交換|塗装|引っ越し).{0,20}(おすすめ|探し|依頼|見積もり|業者|お願い)",
                r"(need|looking for|recommend) (a |an )?(good )?(plumber|electrician|handyman|cleaner|mover)",
            ]
            work_patterns = [
                r"(仕事探し|案件獲得|集客方法|副業|フリーランス|個人事業主).{0,20}(探し|方法|アプリ|おすすめ|困っ|増やし)",
                r"(looking for|need) (side work|handyman work|freelance work)",
            ]
        else:
            # English (+ FR for CA, NL for SR)
            service_patterns = [
                r"(need|looking for|hire|hiring|recommend|recommendations for) (a |an )?(good |reliable |affordable )?(plumber|electrician|handyman|cleaner|house cleaner|painter|carpenter|locksmith|contractor|mover|aircon (servicing|technician|repair))",
                r"(quote|estimate) for (plumbing|electrical|painting|renovation|remodel|repair|cleaning|moving|handyman)",
                r"(besoin d'un|cherche un|recommande(z|r)? un) (bon )?(plombier|[eé]lectricien|peintre|homme [aà] tout faire|femme de m[eé]nage)",
                r"(zoek|gezocht|nodig) (een )?(loodgieter|elektricien|klusjesman|schilder|schoonmaker)",
            ]
            work_patterns = [
                r"(how to|where to|best app to) (get|find) (more )?(clients|customers|leads|handyman jobs|cleaning jobs|plumbing jobs)",
                r"(starting|started) (a |my )?(handyman|cleaning|plumbing|electrical|painting) business",
                r"(looking for|need) (side work|extra income|handyman work|freelance work|odd jobs|gig work)",
                r"offering (handyman|plumbing|electrical|cleaning|painting|moving) services",
                r"(cherche du travail|trouver des clients|travailleur autonome|werk gezocht|klanten vinden)",
            ]

        for pattern in service_patterns:
            if re.search(pattern, text):
                return "SERVICE_SEEKER"
        for pattern in work_patterns:
            if re.search(pattern, text):
                return "WORK_SEEKER"
        return "IRRELEVANT"

    def _draft_heuristic(self, lead_type: str, lang: str) -> str:
        if lang == "pt":
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

        if lang == "es":
            if lead_type == "SERVICE_SEEKER":
                return (
                    f"¡Hola! Si todavía estás buscando, te recomiendo probar {APP_NAME} "
                    f"(Google Play: {GOOGLE_PLAY_URL} | Web: {APP_URL}). "
                    f"Es {APP_VALUE_PROPOSITION_ES_CLIENT}. "
                    "Puedes pedir cotizaciones gratis y comparar reseñas antes de contratar."
                )
            return (
                f"¡Qué tal! Para conseguir más clientes en tu zona, puedes registrarte en {APP_NAME} "
                f"(Google Play: {GOOGLE_PLAY_URL} | Web: {APP_URL}). "
                f"Es {APP_VALUE_PROPOSITION_ES_WORKER}. ¡Mucho éxito!"
            )

        if lang == "fr":
            if lead_type == "SERVICE_SEEKER":
                return (
                    f"Bonjour ! Si vous cherchez toujours un professionnel, essayez {APP_NAME} "
                    f"(Google Play : {GOOGLE_PLAY_URL} | Web : {APP_URL}). "
                    f"C'est {APP_VALUE_PROPOSITION_FR_CLIENT}."
                )
            return (
                f"Bonjour ! Pour trouver plus de clients locaux, inscrivez-vous sur {APP_NAME} "
                f"(Google Play : {GOOGLE_PLAY_URL} | Web : {APP_URL}). "
                f"C'est {APP_VALUE_PROPOSITION_FR_WORKER}."
            )

        if lang == "ja":
            if lead_type == "SERVICE_SEEKER":
                return (
                    f"こんにちは！まだ業者をお探しでしたら、{APP_NAME} をチェックしてみてください"
                    f"（Google Play: {GOOGLE_PLAY_URL} | Web: {APP_URL}）。"
                    f"{APP_VALUE_PROPOSITION_JA_CLIENT}です。"
                )
            return (
                f"こんにちは！地元で新しい案件やお客様を見つけたい場合は、{APP_NAME} への登録もおすすめです"
                f"（Google Play: {GOOGLE_PLAY_URL} | Web: {APP_URL}）。"
                f"{APP_VALUE_PROPOSITION_JA_WORKER}です。"
            )

        if lead_type == "SERVICE_SEEKER":
            return (
                f"Hi! If you're still looking for help, try {APP_NAME} "
                f"(Google Play: {GOOGLE_PLAY_URL} | Web: {APP_URL}). "
                f"It's {APP_VALUE_PROPOSITION_EN_CLIENT}."
            )
        return (
            f"Hey! To find more local jobs and clients in your area, check out {APP_NAME} "
            f"(Google Play: {GOOGLE_PLAY_URL} | Web: {APP_URL}). "
            f"It's {APP_VALUE_PROPOSITION_EN_WORKER}."
        )

    def _analyze_with_gemini(self, title: str, content: str, country: str, platform: str) -> Optional[Tuple[str, Optional[str]]]:
        info = get_country_info(country)
        system_instruction = (
            f"You help the local services app {APP_NAME} (Google Play: {GOOGLE_PLAY_URL}, Web: {APP_URL}) "
            f"in {info['name']}. Classify this {platform} message as SERVICE_SEEKER, WORK_SEEKER, or IRRELEVANT. "
            f"If relevant, write a short (2-3 sentence), natural, non-spammy reply in {info['lang_label']} "
            f"including the Google Play link: {GOOGLE_PLAY_URL}."
        )
        parsed, _ = self.gemini.create_structured_json(
            input_data=f"PLATFORM: {platform}\nCOUNTRY: {info['name']} ({country})\nTITLE: {title}\nCONTENT: {content}",
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
