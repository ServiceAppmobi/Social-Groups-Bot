import os
import shutil

# Brazylia - po portugalsku
SERVICES_BR = [
    ("encanador", "Encanador"),
    ("eletricista", "Eletricista"),
    ("diarista", "Diarista"),
    ("pintor", "Pintor"),
    ("marceneiro", "Marceneiro"),
]
CITIES_BR = [
    ("sao-paulo", "Sao Paulo"),
    ("rio-de-janeiro", "Rio de Janeiro"),
    ("belo-horizonte", "Belo Horizonte"),
    ("brasilia", "Brasilia"),
    ("salvador", "Salvador"),
    ("fortaleza", "Fortaleza"),
    ("curitiba", "Curitiba"),
    ("recife", "Recife"),
    ("porto-alegre", "Porto Alegre"),
    ("manaus", "Manaus"),
    ("belem", "Belem"),
    ("goiania", "Goiania"),
    ("campinas", "Campinas"),
    ("guarulhos", "Guarulhos"),
    ("sao-luis", "Sao Luis"),
    ("maceio", "Maceio"),
    ("natal", "Natal"),
    ("joao-pessoa", "Joao Pessoa"),
    ("teresina", "Teresina"),
    ("florianopolis", "Florianopolis"),
]

# Meksyk - po hiszpansku
SERVICES_MX = [
    ("plomero", "Plomero"),
    ("electricista", "Electricista"),
    ("limpieza", "Limpieza"),
    ("pintor", "Pintor"),
    ("carpintero", "Carpintero"),
]
CITIES_MX = [
    ("ciudad-de-mexico", "Ciudad de Mexico"),
    ("guadalajara", "Guadalajara"),
    ("monterrey", "Monterrey"),
    ("puebla", "Puebla"),
    ("tijuana", "Tijuana"),
    ("merida", "Merida"),
    ("cancun", "Cancun"),
    ("leon", "Leon"),
    ("queretaro", "Queretaro"),
    ("aguascalientes", "Aguascalientes"),
    ("chihuahua", "Chihuahua"),
    ("hermosillo", "Hermosillo"),
    ("culiacan", "Culiacan"),
    ("morelia", "Morelia"),
    ("veracruz", "Veracruz"),
]

MAIN_URL = "https://serviceapp.mobi"
PLAY_LINK = "https://play.google.com/store/apps/details?id=pl.serviceapp"
APPSTORE_LINK = "https://apps.apple.com/ie/app/pl-serviceapp/id1253478797"

PLAY_SMALL = "GET IT ON"
PLAY_BIG = "Goo" + "gle Play"
APPLE_SMALL = "Download on the"
APPLE_BIG = "App" + " Store"

PLAY_SVG = """<svg width="28" height="28" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path fill="#00A0FF" d="M3.6 2.3c-.2.2-.3.5-.3.9v17.6c0 .4.1.7.3.9l9.7-9.7L3.6 2.3z"/><path fill="#FFCE00" d="M17.2 8.2l-3.9 3.8 3.9 3.8 3.3-1.9c.9-.5.9-1.4 0-1.9L17.2 8.2z"/><path fill="#FF3A44" d="M13.3 12l3.9-3.8L5.2.7c-.5-.3-1.1-.2-1.6.1L13.3 12z"/><path fill="#00D173" d="M13.3 12L3.6 21.7c.5.3 1.1.4 1.6.1l11.9-6.6L13.3 12z"/></svg>"""
APPLE_SVG = """<svg width="26" height="30" viewBox="0 0 384 512" xmlns="http://www.w3.org/2000/svg"><path fill="#fff" d="M318.7 268.7c-.2-36.7 16.4-64.4 50-84.8-18.8-26.9-47.2-41.7-84.7-44.6-35.5-2.8-74.3 20.7-88.5 20.7-15 0-49.4-19.7-76.4-19.7C63.3 141.2 4 184.8 4 273.5q0 39.3 14.4 81.2c12.8 36.7 59 126.7 107.2 125.2 25.2-.6 43-17.9 76.8-17.9 31.8 0 48.3 17.9 76.4 17.9 48.6-.7 90.4-82.5 102.6-119.3-65.2-30.7-61.7-90-61.7-91.9zm-56.6-164.2c27.3-32.4 24.8-61.9 24-72.5-24.1 1.4-52 16.4-67.9 34.9-17.5 19.8-27.8 44.3-25.6 71.9 26.1 2 49.9-11.4 69.5-34.3z"/></svg>"""

os.makedirs("_site/landing", exist_ok=True)
if os.path.exists("logo.png"):
    shutil.copy("logo.png", "_site/logo.png")

# Teksty w 2 jezykach
TEXTS = {
    "br": {
        "lang": "pt-BR",
        "need_now": "Precisa de",
        "need_now2": "agora? Peca em 1 minuto, sem procura.",
        "new_order": "Novo pedido de",
        "near_you": "perto de voce",
        "free": "Baixar gratis",
        "no_sub": "Sem assinatura. Sem comissao sobre o pedido.",
        "simple": "Simples, rapido e sem compromisso -",
        "no_search_title": "Sem procura. Sem espera desnecessaria.",
        "no_search_1": "Voce nao precisa procurar prestadores",
        "no_search_1b": "O app faz isso por voce.",
        "no_search_2": "Espera minima",
        "no_search_2b": "Faca o pedido em 1 minuto e acompanhe a resposta.",
        "no_search_3": "Contato imediato",
        "no_search_3b": "Se o prestador aceitar, ele entra em contato imediatamente.",
        "how": "COMO FUNCIONA",
        "how_title": "Tres passos e pronto",
        "step1": "Baixe gratis",
        "step1b": "Instale o ServiceApp no seu celular, sem custo.",
        "step2": "Peca seu servico em 1 minuto",
        "step2b": "Conte o que precisa, sem procurar prestador por prestador.",
        "step3": "O prestador entra em contato imediatamente",
        "step3b": "Ao aceitar o pedido, ele fala direto com voce.",
        "for_pro": "PARA PRESTADORES",
        "for_pro_title": "Receba pedidos prontos para atender",
        "for_pro_b": "Voce recebe o pedido perto de voce, aceita em 1 clique e fala direto com o cliente.",
        "pro1": "Pedidos perto de voce",
        "pro1b": "Raio 2km, 5km ou 10km.",
        "pro2": "Sem mensalidade para comecar",
        "pro2b": "Taxa de aceitacao 29 BRL so quando voce aceita.",
        "pro3": "Promocao para 10, 20, 50 ou 100 pessoas",
        "pro3b": "1 BRL por pessoa. Push ou Push + SMS.",
        "says": "O que dizem em",
        "testi1": "Nao precisei ficar procurando ninguem. Pedi pelo app, o prestador aceitou e me ligou na hora.",
        "testi2": "Pedi em 1 minuto. Em poucos minutos ja tinha resposta e fechei o servico.",
        "faq": "PERGUNTAS FREQUENTES",
        "faq_title": "Duvidas rapidas",
        "faq1q": "Preciso pagar para baixar o app?",
        "faq1a": "Nao. O app e gratis para baixar e usar.",
        "faq2q": "Preciso procurar os profissionais?",
        "faq2a": "Nao. Voce cria o pedido e o app avisa os 10 prestadores mais proximos.",
        "faq3q": "Em quanto tempo recebo o contato?",
        "faq3a": "Assim que um prestador aceitar, ele entra em contato direto com voce.",
        "see_also_city": "Zobacz tez -",
        "see_also_city2": "w innych miastach",
        "other_services": "Inne uslugi w",
        "back_radar": "Wroc do Radar Panel ServiceApp",
        "main_site": "serviceapp.mobi - Strona glowna",
        "download_android": "Pobierz dla Android",
        "download_iphone": "Pobierz dla iPhone",
        "official": "Conta oficial ServiceApp",
        "sticky_free": "Gratis - Pedido em 1 minuto -",
    },
    "mx": {
        "lang": "es-MX",
        "need_now": "Necesitas",
        "need_now2": "ahora? Pidelo en 1 minuto, sin buscar.",
        "new_order": "Nuevo pedido de",
        "near_you": "cerca de ti",
        "free": "Descargar gratis",
        "no_sub": "Sin suscripcion. Sin comision sobre el pedido.",
        "simple": "Simple, rapido y sin compromiso -",
        "no_search_title": "Sin buscar. Sin espera innecesaria.",
        "no_search_1": "No tienes que buscar prestadores",
        "no_search_1b": "La app lo hace por ti.",
        "no_search_2": "Espera minima",
        "no_search_2b": "Haz el pedido en 1 minuto y sigue la respuesta.",
        "no_search_3": "Contacto inmediato",
        "no_search_3b": "Si el prestador acepta, te contacta de inmediato.",
        "how": "COMO FUNCIONA",
        "how_title": "Tres pasos y listo",
        "step1": "Descarga gratis",
        "step1b": "Instala ServiceApp en tu celular, sin costo.",
        "step2": "Pide tu servicio en 1 minuto",
        "step2b": "Cuenta lo que necesitas, sin buscar prestador por prestador.",
        "step3": "El prestador te contacta de inmediato",
        "step3b": "Al aceptar el pedido, habla directo contigo.",
        "for_pro": "PARA PRESTADORES",
        "for_pro_title": "Recibe pedidos listos para atender",
        "for_pro_b": "Recibes el pedido cerca de ti, aceptas en 1 clic y hablas directo con el cliente.",
        "pro1": "Pedidos cerca de ti",
        "pro1b": "Radio 2km, 5km o 10km.",
        "pro2": "Sin mensualidad para empezar",
        "pro2b": "Tarifa de aceptacion 29 MXN solo cuando aceptas.",
        "pro3": "Promocion para 10, 20, 50 o 100 personas",
        "pro3b": "1 MXN por persona. Push o Push + SMS.",
        "says": "Lo que dicen en",
        "testi1": "No tuve que buscar a nadie. Pedi por la app, el prestador acepto y me llamo al momento.",
        "testi2": "Pedi en 1 minuto. En pocos minutos ya tenia respuesta y cerre el servicio.",
        "faq": "PREGUNTAS FRECUENTES",
        "faq_title": "Dudas rapidas",
        "faq1q": "Tengo que pagar para descargar la app?",
        "faq1a": "No. La app es gratis para descargar y usar.",
        "faq2q": "Tengo que buscar a los profesionales?",
        "faq2a": "No. Creas el pedido y la app avisa a los 10 prestadores mas cercanos.",
        "faq3q": "En cuanto tiempo recibo el contacto?",
        "faq3a": "En cuanto un prestador acepte, te contacta directo.",
        "see_also_city": "Ver tambien -",
        "see_also_city2": "en otras ciudades",
        "other_services": "Otros servicios en",
        "back_radar": "Volver al Radar Panel ServiceApp",
        "main_site": "serviceapp.mobi - Sitio principal",
        "download_android": "Descargar para Android",
        "download_iphone": "Descargar para iPhone",
        "official": "Cuenta oficial ServiceApp",
        "sticky_free": "Gratis - Pedido en 1 minuto -",
    }
}

def make_page(service_pt, service_pl, city_slug, city_name, country, services_list, cities_list):
    t = TEXTS[country]
    prefix = "br" if country == "br" else "mx"
    slug = f"{prefix}-{service_pt}-{city_slug}"
    path = f"_site/landing/{slug}"
    os.makedirs(path, exist_ok=True)

    city_links = "".join([f'<a href="../{prefix}-{service_pt}-{c2}/" style="display:block;background:#eff6ff;color:#1e40af;padding:12px 14px;border-radius:12px;text-decoration:underline;font-weight:700">{service_pl} {n2} -></a>' for c2, n2 in cities_list if c2 != city_slug])
    service_links = "".join([f'<a href="../{prefix}-{pt2}-{city_slug}/" style="display:block;background:#eff6ff;color:#1e40af;padding:12px 14px;border-radius:12px;text-decoration:underline;font-weight:700">{pl2} {city_name} -></a>' for pt2, pl2 in services_list if pt2 != service_pt])

    html = f"""<!DOCTYPE html>
<html lang="{t['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{service_pl} em {city_name} | ServiceApp</title>
<meta name="description" content="{t['need_now']} {service_pt} {t['need_now2']}">
<style>
*{{box-sizing:border-box}} body{{margin:0;font-family:Arial,sans-serif;background:#f8fafc;color:#0f172a}}
.top{{display:flex;align-items:center;justify-content:space-between;padding:14px 16px;background:#fff;border-bottom:1px solid #e0eafb;position:sticky;top:0;z-index:10}}
.logo{{display:flex;align-items:center;gap:10px;font-size:22px;font-weight:900}} .logo img{{width:42px;height:42px;border-radius:10px;object-fit:cover}}
.badge{{background:#eff6ff;color:#1e40af;font-size:12px;font-weight:700;padding:8px 12px;border-radius:999px}}
.wrap{{max-width:520px;margin:0 auto;padding:16px 12px 120px}}
.card{{background:#fff;border:1px solid #dbeafe;border-radius:28px;padding:22px 20px}}
.pill{{display:inline-block;background:#eff6ff;color:#1e40af;font-weight:700;font-size:13px;padding:8px 12px;border-radius:999px;margin:14px 0}}
h1{{font-size:44px;line-height:.95;letter-spacing:-1.5px;margin:14px 0 12px}} .lead{{color:#64748b;font-size:20px;line-height:1.35}}
.btn-blue{{display:flex;align-items:center;justify-content:center;text-align:center;background:linear-gradient(90deg,#38bdf8,#2563eb 55%,#1e40af);color:#fff;text-decoration:none;font-weight:800;font-size:20px;height:56px;border-radius:20px;width:100%}}
.note{{text-align:center;color:#64748b;font-size:15px;margin:14px 0 16px}}
.stores{{display:flex;gap:10px;width:100%}}
.store-badge{{flex:1 1 0;min-width:0;height:64px;background:#000;color:#fff;border:1px solid #a6a6a6;border-radius:10px;padding:8px 10px;display:flex;align-items:center;justify-content:center;gap:10px;text-decoration:none;overflow:hidden}}
.store-badge .badge-icon{{flex-shrink:0;display:flex;align-items:center;justify-content:center}}
.store-badge .badge-text{{display:flex;flex-direction:column;align-items:flex-start;line-height:1.1;min-width:0}}
.store-badge .badge-text small{{font-size:10px;letter-spacing:1px;text-transform:uppercase;color:#fff;font-weight:400}}
.store-badge .badge-text b{{font-size:19px;font-weight:700;white-space:nowrap;letter-spacing:-0.2px}}
.mini{{background:#f0f7ff;border:1px solid #dbeafe;border-radius:20px;padding:16px;display:flex;gap:14px;margin-top:14px}}
.how{{background:linear-gradient(180deg,#0ea5e9,#2563eb 55%,#1e40af);color:#fff;border-radius:32px;padding:28px 22px;margin-top:28px}} .how h2{{color:#fff}} .step{{display:flex;gap:16px;margin-top:24px}} .num{{width:52px;height:52px;background:#fff;color:#1e40af;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:22px;flex-shrink:0}} .step p{{color:#dbeafe}}
.testi{{background:#f0f7ff;border:1px solid #dbeafe;border-radius:22px;padding:18px;margin-top:14px}} .stars{{color:#f59e0b;font-size:20px;letter-spacing:3px}}
.faq{{background:#f0f7ff;border:1px solid #dbeafe;border-radius:20px;padding:16px;margin-top:12px}} .faq summary{{font-weight:800;cursor:pointer;display:flex;justify-content:space-between}}
.sticky{{position:fixed;left:0;right:0;bottom:0;background:#fff;border-top:1px solid #e2e8f0;padding:12px 14px;display:flex;align-items:center;justify-content:space-between;gap:12px;z-index:20}} .sticky .btn-blue{{height:48px;padding:0 18px;font-size:17px;flex-shrink:0;min-width:150px}}
</style></head><body>
<div class="top"><div class="logo"><a href="{MAIN_URL}" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;text-decoration:none;color:#0f172a"><img src="../../logo.png"><span>Service<b style="color:#2563eb">App</b></span></a></div><div class="badge">{t['official']}</div></div>
<div class="wrap"><div class="card">
<div style="display:flex;gap:12px;align-items:flex-start"><a href="{MAIN_URL}" target="_blank" rel="noopener"><img src="../../logo.png" style="width:52px;height:52px;border-radius:50%;object-fit:cover"></a><div><b style="font-size:18px">ServiceApp</b><div style="color:#64748b;font-size:14px">{t['new_order']} {service_pt} {t['near_you']}</div></div><div style="color:#64748b;font-size:14px;margin-left:auto">agora</div></div>
<div class="pill">Projeto para aprovacao - <a href="{MAIN_URL}" target="_blank" rel="noopener" style="color:#1e40af">serviceapp.mobi</a></div>
<h1>{service_pl} em {city_name}</h1><p class="lead">{t['need_now']} {service_pt} {t['need_now2']}</p>
<a class="btn-blue" href="{PLAY_LINK}" target="_blank" rel="noopener">{t['free']}</a><p class="note">{t['no_sub']}</p>
<div class="stores"><a class="store-badge" href="{PLAY_LINK}" target="_blank" rel="noopener"><span class="badge-icon">{PLAY_SVG}</span><span class="badge-text"><small>{PLAY_SMALL}</small><b>{PLAY_BIG}</b></span></a><a class="store-badge" href="{APPSTORE_LINK}" target="_blank" rel="noopener"><span class="badge-icon">{APPLE_SVG}</span><span class="badge-text"><small>{APPLE_SMALL}</small><b>{APPLE_BIG}</b></span></a></div>
<div style="text-align:center;color:#64748b;font-size:14px;margin-top:18px;border-top:1px solid #e2e8f0;padding-top:16px">{t['simple']} <a href="{MAIN_URL}" target="_blank" rel="noopener" style="color:#2563eb;font-weight:700">serviceapp.mobi</a></div></div>
<div style="margin-top:28px"><h2 style="font-size:32px">{t['no_search_title']}</h2>
<div class="mini"><div><b>{t['no_search_1']}</b><p style="color:#64748b">{t['no_search_1b']}</p></div></div>
<div class="mini"><div><b>{t['no_search_2']}</b><p style="color:#64748b">{t['no_search_2b']}</p></div></div>
<div class="mini"><div><b>{t['no_search_3']}</b><p style="color:#64748b">{t['no_search_3b']}</p></div></div></div>
<div class="how"><div style="color:#bae6fd;font-weight:800;letter-spacing:2px;font-size:13px">{t['how']}</div><h2 style="font-size:32px">{t['how_title']}</h2>
<div class="step"><div class="num">1</div><div><h3>{t['step1']}</h3><p>{t['step1b']} <a href="{PLAY_LINK}" target="_blank" rel="noopener" style="color:#fff;font-weight:700">Android</a> / <a href="{APPSTORE_LINK}" target="_blank" rel="noopener" style="color:#fff;font-weight:700">iPhone</a></p></div></div>
<div class="step"><div class="num">2</div><div><h3>{t['step2']}</h3><p>{t['step2b']}</p></div></div>
<div class="step"><div class="num">3</div><div><h3>{t['step3']}</h3><p>{t['step3b']}</p></div></div></div>
<div style="margin-top:28px"><div style="color:#2563eb;font-weight:800;letter-spacing:2px;font-size:13px">{t['for_pro']}</div><h2 style="font-size:32px">{t['for_pro_title']}</h2><p style="color:#64748b">{t['for_pro_b']}</p>
<div class="mini"><div><b>{t['pro1']}</b><p style="color:#64748b">{t['pro1b']}</p></div></div>
<div class="mini"><div><b>{t['pro2']}</b><p style="color:#64748b">{t['pro2b']}</p></div></div>
<div class="mini"><div><b>{t['pro3']}</b><p style="color:#64748b">{t['pro3b']}</p></div></div></div>
<div style="margin-top:28px"><h2 style="font-size:32px">{t['says']} {city_name}</h2>
<div class="testi"><div class="stars">★★★★★</div><p>{t['testi1']}</p><b>Joao</b> <span style="color:#64748b">{city_name}</span></div>
<div class="testi"><div class="stars">★★★★★</div><p>{t['testi2']}</p><b>Maria</b> <span style="color:#64748b">{city_name}</span></div></div>
<div style="margin-top:28px"><div style="color:#2563eb;font-weight:800;letter-spacing:2px;font-size:13px">{t['faq']}</div><h2 style="font-size:32px">{t['faq_title']}</h2>
<details class="faq" open><summary>{t['faq1q']} <span>^</span></summary><p style="color:#64748b">{t['faq1a']} <a href="{PLAY_LINK}" target="_blank" rel="noopener">Android</a> / <a href="{APPSTORE_LINK}" target="_blank" rel="noopener">iPhone</a></p></details>
<details class="faq"><summary>{t['faq2q']} <span>></span></summary><p style="color:#64748b">{t['faq2a']}</p></details>
<details class="faq"><summary>{t['faq3q']} <span>></span></summary><p style="color:#64748b">{t['faq3a']}</p></details></div>
<div style="margin-top:28px;background:#fff;border:2px solid #2563eb;border-radius:20px;padding:20px">
<h3 style="color:#1e40af;margin:0 0 12px">{t['see_also_city']} {service_pl} {t['see_also_city2']}</h3>
<div style="display:flex;flex-direction:column;gap:10px">{city_links}</div>
<h3 style="color:#1e40af;margin:20px 0 12px">{t['other_services']} {city_name}</h3>
<div style="display:flex;flex-direction:column;gap:10px">{service_links}</div>
<p style="margin-top:16px"><a href="../../" target="_blank" rel="noopener" style="color:#2563eb;font-weight:800">{t['back_radar']}</a></p>
<p><a href="{MAIN_URL}" target="_blank" rel="noopener" style="color:#2563eb;font-weight:800">{t['main_site']}</a></p>
<p><a href="{PLAY_LINK}" target="_blank" rel="noopener" style="color:#2563eb;font-weight:800">{t['download_android']}</a></p>
<p><a href="{APPSTORE_LINK}" target="_blank" rel="noopener" style="color:#2563eb;font-weight:800">{t['download_iphone']}</a></p>
</div>
<div style="text-align:center;padding:28px 0;color:#64748b"><div style="display:flex;align-items:center;justify-content:center;gap:10px;font-size:20px;font-weight:900;color:#0f172a"><a href="{MAIN_URL}" target="_blank" rel="noopener"><img src="../../logo.png" style="width:36px;height:36px;border-radius:8px;object-fit:cover"></a> Service<span style="color:#2563eb">App</span></div><p>{t['official']}</p><a href="{MAIN_URL}" target="_blank" rel="noopener" style="color:#1e40af;font-weight:800">serviceapp.mobi</a></div></div>
<div class="sticky"><div><b>{service_pl} em {city_name}</b><div style="color:#64748b;font-size:14px">{t['sticky_free']} <a href="{MAIN_URL}" target="_blank" rel="noopener" style="color:#2563eb">serviceapp.mobi</a></div></div><a class="btn-blue" href="{PLAY_LINK}" target="_blank" rel="noopener">{t['free']}</a></div>
</body></html>"""
    open(f"{path}/index.html", "w", encoding="utf-8").write(html)
    return f"landing/{slug}/"

pages = []
for pt, pl in SERVICES_BR:
    for c_slug, c_name in CITIES_BR:
        pages.append(make_page(pt, pl, c_slug, c_name, "br", SERVICES_BR, CITIES_BR))
for pt, pl in SERVICES_MX:
    for c_slug, c_name in CITIES_MX:
        pages.append(make_page(pt, pl, c_slug, c_name, "mx", SERVICES_MX, CITIES_MX))

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in pages:
    sitemap += f"<url><loc>{u}</loc></url>\n"
sitemap += f"<url><loc>{MAIN_URL}/</loc></url>\n</urlset>"
open("_site/sitemap.xml", "w", encoding="utf-8").write(sitemap)
open("_site/robots.txt", "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nSitemap: sitemap.xml\n")
print(f"Created {len(pages)} landing pages - BR {len(SERVICES_BR)*len(CITIES_BR)} + MX {len(SERVICES_MX)*len(CITIES_MX)}")
