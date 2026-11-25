import os

SERVICES = [
    ("hydraulik", "Hydraulik", "encanador"),
    ("elektryk", "Elektryk", "eletricista"),
    ("sprzatanie", "Sprzatanie", "diarista"),
    ("malarz", "Malarz", "pintor"),
    ("stolarz", "Stolarz", "marceneiro"),
]

CITIES = [
    ("sao-paulo", "Sao Paulo"),
    ("campinas", "Campinas"),
    ("manaus", "Manaus"),
    ("belo-horizonte", "Belo Horizonte"),
]

BASE_URL = "https://serviceappmobi.github.io/Social-Groups-Bot"
PLAY_LINK = "https://play.google.com/store/apps/details?id=com.serviceapp"

os.makedirs("_site/landing", exist_ok=True)

pages = []

for service_slug, service_pl, service_pt in SERVICES:
    for city_slug, city_name in CITIES:
        slug = f"{service_pt}-{city_slug}"
        path = f"_site/landing/{slug}"
        os.makedirs(path, exist_ok=True)
        url = f"{BASE_URL}/landing/{slug}/"
        pages.append(url)

        # Linki do innych miast dla SEO
        other_links = "".join([f'<li><a href="../{service_pt}-{c2}/">{service_pl} {n2}</a></li>' for c2, n2 in CITIES if c2 != city_slug])

        html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>{service_pl} {city_name} - Znajdz fachowca w 15 minut | ServiceApp</title>
<meta name="description" content="Preciso de {service_pt} em {city_name}? W ServiceApp 10 najblizszych fachowcow dostaje powiadomienie od razu. Zamow w 1 klikniecie.">
</head>
<body style="font-family:Arial;max-width:800px;margin:40px auto;padding:20px">
<h1>Preciso de {service_pt} em {city_name}?</h1>
<p>W ServiceApp nie musisz szukac na forach i czekac. Tworzysz Service Request, a 10 najblizszych fachowcow w {city_name} dostaje powiadomienie Push i SMS od razu. Pierwszy, ktory zaakceptuje, przyjezdza do Ciebie.</p>
<h2>Dlaczego ServiceApp w {city_name}?</h2>
<ul>
<li>10 najblizszych fachowcow dostaje Twoje zlecenie</li>
<li>Platnosc i akceptacja zlecenia w aplikacji, oplata akceptacyjna 29 BRL</li>
<li>Fachowcy moga sie sami promowac do 15, 20, 50 lub 100 osob w okolicy za 1 BRL za osobe</li>
<li>Obszar: 2km, 5km lub 10km</li>
</ul>
<a href="{PLAY_LINK}" style="background:#22c55e;color:white;padding:14px 24px;text-decoration:none;border-radius:10px;display:inline-block">Pobierz ServiceApp z Google Play</a>
<h3>Inne miasta</h3>
<ul>{other_links}</ul>
<p><a href="../../">Wroc do Radar Panel ServiceApp</a></p>
</body>
</html>"""
        open(f"{path}/index.html", "w", encoding="utf-8").write(html)

# sitemap.xml - to jest klucz do indeksowania
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in pages:
    sitemap += f"<url><loc>{u}</loc></url>\n"
sitemap += f"<url><loc>{BASE_URL}/</loc></url>\n</urlset>"
open("_site/sitemap.xml", "w", encoding="utf-8").write(sitemap)

# robots.txt
open("_site/robots.txt", "w", encoding="utf-8").write("User-agent: *\nAllow: /\nSitemap: " + BASE_URL + "/sitemap.xml\n")

print(f"Created {len(pages)} landing pages")
