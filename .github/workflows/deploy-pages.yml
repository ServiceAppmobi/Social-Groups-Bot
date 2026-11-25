import os
import shutil

SERVICES = [
    ("encanador", "Encanador"),
    ("eletricista", "Eletricista"),
    ("diarista", "Diarista"),
    ("pintor", "Pintor"),
    ("marceneiro", "Marceneiro"),
]
CITIES = [
    ("sao-paulo", "São Paulo"),
    ("campinas", "Campinas"),
    ("manaus", "Manaus"),
    ("belo-horizonte", "Belo Horizonte"),
]

BASE_URL = "https://serviceappmobi.github.io/Social-Groups-Bot"
PLAY_LINK = "https://play.google.com/store/apps/details?id=com.serviceapp"
APPSTORE_LINK = "https://apps.apple.com/app/serviceapp"
LOGO_URL = f"{BASE_URL}/logo.png"

# Oryginalne ikonki - 【entity-Apple¦canonical_name=Apple】 i 【entity-Google Play¦canonical_name=Google Play】 jako SVG, nie emoji
APPLE_SVG = [STRIPPED 518 bytes]
PLAY_SVG = [STRIPPED 316 bytes]

os.makedirs("_site/landing", exist_ok=True)
# Kopiuj oryginalne logo do _site, żeby było na 【entity-GitHub¦canonical_name=GitHub】 Pages
if os.path.exists("logo.png"):
    shutil.copy("logo.png", "_site/logo.png")

def make_page(service_pt, service_pl, city_slug, city_name):
    slug = f"{service_pt}-{city_slug}"
    path = f"_site/landing/{slug}"
    os.makedirs(path, exist_ok=True)

    city_links = "".join([f'<a href="{BASE_URL}/landing/{service_pt}-{c2}/">{service_pl} {n2} →</a>' for c2, n2 in CITIES if c2 != city_slug])
    service_links = "".join([f'<a href="{BASE_URL}/landing/{pt2}-{city_slug}/">{pl2} {city_name} →</a>' for pt2, pl2 in SERVICES if pt2 != service_pt])

    html = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{service_pl} em {city_name} | ServiceApp</title>
<meta name="description" content="Precisa de {service_pt} agora? Peça em 1 minuto, sem procura.">
<style>
*{{box-sizing:border-box}} body{{margin:0;font-family:Arial,sans-serif;background:#f8fafc;color:#0f172a}}
.top{{display:flex;align-items:center;justify-content:space-between;padding:14px 16px;background:#fff;border-bottom:1px solid #e0eafb;position:sticky;top:0;z-index:10}}
.logo{{display:flex;align-items:center;gap:10px;font-size:22px;font-weight:900}} .logo img{{width:42px;height:42px;border-radius:10px;object-fit:cover}}
.badge{{background:#eff6ff;color:#1e40af;font-size:12px;font-weight:700;padding:8px 12px;border-radius:999px}}
.wrap{{max-width:520px;margin:0 auto;padding:16px 12px 120px}}
.card{{background:#fff;border:1px solid #dbeafe;border-radius:28px;padding:22px 20px}}
.pill{{display:inline-block;background:#eff6ff;color:#1e40af;font-weight:700;font-size:13px;padding:8px 12px;border-radius:999px;margin:14px 0}}
h1{{font-size:44px;line-height:.95;letter-spacing:-1.5px;margin:14px 0 12px}} .lead{{color:#64748b;font-size:20px;line-height:1.35}}
.btn-blue{{display:block;text-align:center;background:linear-gradient(90deg,#38bdf8,#2563eb 55%,#1e40af);color:#fff;text-decoration:none;font-weight:800;font-size:22px;padding:18px;border-radius:20px}}
.note{{text-align:center;color:#64748b;font-size:15px;margin:14px 0 16px}}
.stores{{display:flex;gap:10px}} .store{{flex:1;background:#0f172a;color:#fff;border-radius:16px;padding:14px 10px;display:flex;align-items:center;justify-content:center;gap:10px;text-decoration:none}} .store small{{display:block;font-size:12px;color:#cbd5e1}} .store b{{font-size:18px}}
.mini{{background:#f0f7ff;border:1px solid #dbeafe;border-radius:20px;padding:16px;display:flex;gap:14px;margin-top:14px}}
.how{{background:linear-gradient(180deg,#0ea5e9,#2563eb 55%,#1e40af);color:#fff;border-radius:32px;padding:28px 22px;margin-top:28px}} .how h2{{color:#fff}} .step{{display:flex;gap:16px;margin-top:24px}} .num{{width:52px;height:52px;background:#fff;color:#1e40af;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:22px;flex-shrink:0}} .step p{{color:#dbeafe}}
.testi{{background:#f0f7ff;border:1px solid #dbeafe;border-radius:22px;padding:18px;margin-top:14px}} .stars{{color:#f59e0b;font-size:20px;letter-spacing:3px}}
.faq{{background:#f0f7ff;border:1px solid #dbeafe;border-radius:20px;padding:16px;margin-top:12px}} .faq summary{{font-weight:800;cursor:pointer;display:flex;justify-content:space-between}}
.links{{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}} .links a{{background:#e0f2fe;color:#1e40af;padding:8px 12px;border-radius:999px;text-decoration:none;font-size:13px;font-weight:700}}
.sticky{{position:fixed;left:0;right:0;bottom:0;background:#fff;border-top:1px solid #e2e8f0;padding:12px 14px;display:flex;align-items:center;justify-content:space-between;gap:12px;z-index:20}} .sticky .btn-blue{{padding:14px 18px;font-size:18px}}
</style></head><body>
<div class="top"><div class="logo"><img src="{LOGO_URL}"><span>Service<b style="color:#2563eb">App</b></span></div><div class="badge">✓ Conta oficial ServiceApp</div></div>
<div class="wrap"><div class="card">
<div style="display:flex;gap:12px;align-items:flex-start"><img src="{LOGO_URL}" style="width:52px;height:52px;border-radius:50%;object-fit:cover"><div><b style="font-size:18px">ServiceApp</b><div style="color:#64748b;font-size:14px">Novo pedido de {service_pt} perto de você</div></div><div style="color:#64748b;font-size:14px;margin-left:auto">agora</div></div>
<div class="pill">✦ Projeto para aprovação • serviceapp.mobi</div>
<h1>{service_pl} em {city_name}</h1><p class="lead">Precisa de {service_pt} agora? Peça em 1 minuto, sem procura.</p>
<a class="btn-blue" href="{PLAY_LINK}">↓ Baixar grátis</a><p class="note">Sem assinatura. Sem comissão sobre o pedido.</p>
<div class="stores"><a class="store" href="{APPSTORE_LINK}">{APPLE_SVG}<span><small>Baixar na</small><b>App Store</b></span></a><a class="store" href="{PLAY_LINK}">{PLAY_SVG}<span><small>Baixar no</small><b>【entity-Google Play¦canonical_name=Google Play】</b></span></a></div>
<div style="text-align:center;color:#64748b;font-size:14px;margin-top:18px;border-top:1px solid #e2e8f0;padding-top:16px">🛡 Simples, rápido e sem compromisso</div></div>
<div style="margin-top:28px"><h2 style="font-size:32px">Sem procura. Sem espera desnecessária.</h2>
<div class="mini"><div><b>Você não precisa procurar prestadores</b><p style="color:#64748b">O app faz isso por você.</p></div></div>
<div class="mini"><div><b>Espera mínima</b><p style="color:#64748b">Faça o pedido em 1 minuto e acompanhe a resposta.</p></div></div>
<div class="mini"><div><b>Contato imediato</b><p style="color:#64748b">Se o prestador aceitar, ele entra em contato imediatamente.</p></div></div></div>
<div class="how"><div style="color:#bae6fd;font-weight:800;letter-spacing:2px;font-size:13px">COMO FUNCIONA</div><h2 style="font-size:32px">Três passos e pronto</h2>
<div class="step"><div class="num">1</div><div><h3>Baixe grátis</h3><p>Instale o ServiceApp no seu celular, sem custo.</p></div></div>
<div class="step"><div class="num">2</div><div><h3>Peça seu serviço em 1 minuto</h3><p>Conte o que precisa, sem procurar prestador por prestador.</p></div></div>
<div class="step"><div class="num">3</div><div><h3>O prestador entra em contato imediatamente</h3><p>Ao aceitar o pedido, ele fala direto com você.</p></div></div></div>
<div style="margin-top:28px"><div style="color:#2563eb;font-weight:800;letter-spacing:2px;font-size:13px">PARA PRESTADORES</div><h2 style="font-size:32px">Receba pedidos prontos para atender</h2><p style="color:#64748b">Você recebe o pedido perto de você, aceita em 1 clique e fala direto com o cliente.</p>
<div class="mini"><div><b>Pedidos perto de você</b><p style="color:#64748b">Raio 2km, 5km ou 10km.</p></div></div>
<div class="mini"><div><b>Sem mensalidade para começar</b><p style="color:#64748b">Taxa de aceitação 29 BRL só quando você aceita.</p></div></div>
<div class="mini"><div><b>Promoção para 10, 20, 50 ou 100 pessoas</b><p style="color:#64748b">1 BRL por pessoa. Push ou Push + SMS.</p></div></div></div>
<div style="margin-top:28px"><h2 style="font-size:32px">O que dizem em {city_name}</h2>
<div class="testi"><div class="stars">★★★★★</div><p>“Não precisei ficar procurando ninguém. Pedi pelo app, o prestador aceitou e me ligou na hora.”</p><b>João</b> <span style="color:#64748b">{city_name}</span></div>
<div class="testi"><div class="stars">★★★★★</div><p>“Pedi em 1 minuto. Em poucos minutos já tinha resposta e fechei o serviço.”</p><b>Maria</b> <span style="color:#64748b">{city_name}</span></div></div>
<div style="margin-top:28px"><div style="color:#2563eb;font-weight:800;letter-spacing:2px;font-size:13px">PERGUNTAS FREQUENTES</div><h2 style="font-size:32px">Dúvidas rápidas</h2>
<details class="faq" open><summary>Preciso pagar para baixar o app? <span>^</span></summary><p style="color:#64748b">Não. O app é grátis para baixar e usar.</p></details>
<details class="faq"><summary>Preciso procurar os profissionais? <span>⌄</span></summary><p style="color:#64748b">Não. Você cria o pedido e o app avisa os 10 prestadores mais próximos.</p></details>
<details class="faq"><summary>Em quanto tempo recebo o contato? <span>⌄</span></summary><p style="color:#64748b">Assim que um prestador aceitar, ele entra em contato direto com você.</p></details></div>
<div style="margin-top:28px"><h3>Outras cidades - {service_pl}</h3><div class="links">{city_links}</div><h3 style="margin-top:18px">Outros serviços em {city_name}</h3><div class="links">{service_links}</div></div>
<div style="text-align:center;padding:28px 0;color:#64748b"><div style="display:flex;align-items:center;justify-content:center;gap:10px;font-size:20px;font-weight:900;color:#0f172a"><img src="{LOGO_URL}" style="width:36px;height:36px;border-radius:8px;object-fit:cover"> Service<span style="color:#2563eb">App</span></div><p>✓ Conta oficial ServiceApp</p><a href="https://serviceapp.mobi" style="color:#1e40af;font-weight:800">serviceapp.mobi</a></div></div>
<div class="sticky"><div><b>{service_pl} em {city_name}</b><div style="color:#64748b;font-size:14px">Grátis • Pedido em 1 minuto</div></div><a class="btn-blue" href="{PLAY_LINK}">↓ Baixar grátis</a></div>
</body></html>"""
    open(f"{path}/index.html", "w", encoding="utf-8").write(html)
    return f"{BASE_URL}/landing/{slug}/"

pages = []
for pt, pl in SERVICES:
    for c_slug, c_name in CITIES:
        pages.append(make_page(pt, pl, c_slug, c_name))

# Sitemap + robots dla Google
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in pages:
    sitemap += f"<url><loc>{u}</loc></url>\n"
sitemap += f"<url><loc>{BASE_URL}/</loc></url>\n</urlset>"
open("_site/sitemap.xml", "w", encoding="utf-8").write(sitemap)
open("_site/robots.txt", "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n")
print(f"Created {len(pages)} landing pages")
