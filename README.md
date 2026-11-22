# 📱 ServiceApp Social Groups Bot (WhatsApp, Facebook Groups & TikTok — BR & MX)

Drugi dedykowany bot dla **ServiceApp** (zero zależności zewnętrznych, Python 3.9+, 0 zł na GitHub Actions) nastawiony na kanały **WhatsApp grupy**, **Facebook grupy** oraz **TikTok** w Brazylii (PT-BR) i Meksyku (ES-MX).

Każda wygenerowana propozycja odpowiedzi zawiera bezpośredni link do Google Play:
**`https://play.google.com/store/apps/details?id=pl.serviceapp&pli=1`**

---

## Jak działają poszczególne kanały (uczciwie i zgodnie z zasadami platform)

Meta (Facebook/WhatsApp) oraz TikTok **nie udostępniają darmowego API do automatycznego przeszukiwania prywatnych grup ani profili** i blokują scrapery. Dlatego bot łączy **4 dozwolone mechanizmy**:

1. **Publiczne RSS (działa automatycznie co 4h na GitHub Actions za 0 zł):**
   - Wyszukuje wyłącznie publicznie indeksowane wzmianki `facebook.com`, `tiktok.com` i grup WhatsApp w Brazylii i Meksyku.
2. **Webhook w czasie rzeczywistym dla grup WhatsApp, Facebooka i TikToka (`python3 main.py --webhook`):**
   - `POST /webhook/whatsapp` — podpinasz bramkę WhatsApp (Evolution API / WPPConnect / Baileys) dla grup, do których należysz.
   - `POST /webhook/facebook` oraz `POST /webhook/tiktok` — podpinasz oficjalne webhooki lub scenariusze Make/n8n.
3. **Importer eksportów czatów WhatsApp (`--import-whatsapp plik.txt`):**
   - W WhatsApp klikasz *Eksportuj czat (bez multimediów)* i uruchamiasz bota na pliku `.txt` — od razu wyciąga leady i generuje gotowe odpowiedzi z linkiem do Google Play.
4. **Panel 1-klik (`dashboard.html` / `http://localhost:8089/dashboard`):**
   - Gotowe linki wyszukiwania do Facebook Groups i TikTok (BR & MX) + przyciski kopiowania odpowiedzi PT-BR / ES-MX z linkiem Google Play.

---

## Szybki start (zero `pip install`)

```bash
# Test demonstracyjny (WhatsApp + Facebook + TikTok dla BR i MX)
python3 main.py --mock --dry-run

# Skanowanie publicznych wzmianek RSS
python3 main.py --dry-run

# Analiza wyeksportowanego czatu grupy WhatsApp
python3 main.py --import-whatsapp czat_grupy.txt --country BR --dry-run

# Serwer webhooków + panel HTML (http://localhost:8089/dashboard)
python3 main.py --webhook

# Testy jednostkowe
python3 -m unittest test_social_groups_bot.py -v
```
