# ServiceApp - Bot do pozyskiwania KLIENTOW
# BEZPIECZNY: nic nie wysyla sam. Tylko przygotowuje odpowiedzi.

import os, re
from datetime import datetime, timezone

KEYWORDS = [
    "procuro encanador", "procuro eletricista", "procuro faxina",
    "preciso de encanador", "preciso de eletricista", "preciso de pedreiro",
    "szukam hydraulika", "szukam elektryka", "szukam sprzatanie",
    "busco plomero", "busco electricista", "necesito plomero",
]

REPLY_PT = """Oi! Vi que você está procurando {servico} em {cidade}.

Você não precisa procurar prestadores, o aplicativo faz isso para você.
Crie sua solicitação em 10-20 segundos no ServiceApp e um prestador aceita e entra em contato com você imediatamente.

Tempo de espera reduzido ao mínimo.
Aplicativo gratuito, sem mensalidade.

Baixe ServiceApp, link na bio. Posso te ajudar a criar o pedido?"""

def clean(t):
    return re.sub(r'\s+', ' ', t or '').strip()

def wykryj_usluge(text):
    t = text.lower()
    if "encanador" in t or "hydraulika" in t or "plomero" in t:
        return "encanador"
    if "eletricista" in t or "elektryka" in t or "electricista" in t:
        return "eletricista"
    if "faxina" in t or "sprzatanie" in t:
        return "faxina"
    if "pedreiro" in t:
        return "pedreiro"
    return "serviço"

def wykryj_miasto(text):
    for miasto in ["São Paulo", "Sao Paulo", "Rio de Janeiro", "Belo Horizonte", "Curitiba", "Brasília"]:
        if miasto.lower() in text.lower():
            return miasto
    return "sua cidade"

def main():
    posty = []
    if os.path.exists("examples.txt"):
        with open("examples.txt", encoding="utf-8") as f:
            posty = [clean(l) for l in f if clean(l)]
    if not posty:
        posty = ["Procuro encanador em São Paulo urgente, alguém indica?"]

    gotowe = []
    for post in posty:
        if not any(k.lower() in post.lower() for k in KEYWORDS):
            continue
        gotowe.append({
            "post": post,
            "odpowiedz": REPLY_PT.format(servico=wykryj_usluge(post), cidade=wykryj_miasto(post))
        })

    os.makedirs("out", exist_ok=True)
    with open("out/drafts.md", "w", encoding="utf-8") as f:
        f.write("# ServiceApp - Gotowe odpowiedzi dla KLIENTOW\n\n")
        f.write(f"Znaleziono: {len(gotowe)}\n\n")
        f.write("ZASADA: Max 5-10 odpowiedzi dziennie.\n\n---\n\n")
        for i, d in enumerate(gotowe, 1):
            f.write(f"## {i}. Post: {d['post']}\n\n```\n{d['odpowiedz']}\n```\n\n---\n\n")
    print(f"OK: {len(gotowe)} gotowych odpowiedzi")

if __name__ == "__main__":
    main()
