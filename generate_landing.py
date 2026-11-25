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
    ("sao-paulo", "Sao Paulo"),
    ("campinas", "Campinas"),
    ("manaus", "Manaus"),
    ("belo-horizonte", "Belo Horizonte"),
]

MAIN_URL = "https://serviceapp.mobi"
PLAY_LINK = "https://play.google.com/store/apps/details?id=pl.serviceapp"
APPSTORE_LINK = "https://apps.apple.com/ie/app/pl-serviceapp/id1253478797"

os.makedirs("_site/landing", exist_ok=True)
if os.path.exists("logo.png"):
    shutil.copy("logo.png", "_site/logo.png")

def make_page(service_pt, service_pl, city_slug, city_name):
    slug = f"{service_pt}-{city_slug}"
    path = f"_site/landing/{slug}"
    os.makedirs(path, exist_ok=True)

    city_links = "".join([f'<a href="../{service_pt}-{c2}/" style="display:block;background:#eff6ff;color:#1e40af;padding:12px 14px;border-radius:12px;text-decoration:underline;font-weight:700">{service_pl} {n2} -></a>' for c2, n2 in CITIES if c2 != city_slug])
    service_links = "".join([f'<a href="../{pt2}-{city_slug}/" style="display:block;background:#eff6ff;color:#1e40af;padding:12px 14px;border-radius:12px;text-decoration:underline;font-weight:700">{pl2} {city_name} -></a>' for pt2, pl2 in SERVICES if pt2 != service_pt])

    html = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{service_pl} em {city_name} | ServiceApp</title>
<meta name="description" content="Precisa de {service_pt} agora? Peca em 1 minuto, sem procura.">
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
.store{{flex:1 1 0;min-width:0;height:58px;background:#0f172a;color:#fff;border-radius:16px;padding:0 8px;display:flex;align-items:center;justify-content:center;gap:6px;text-decoration:none;font-size:15px;font-weight:800;white-space:nowrap;overflow:hidden}}
.store small{{font-size:13px;font-weight:400;color:#cbd5e1;white-space:nowrap}}
.mini{{background:#f0f7ff;border:1px solid #dbeafe;border-radius:20px;padding:16px;display:flex;gap:14px;margin-top:14px}}
.how{{background:linear-gradient(180deg,#0ea5e9,#2563eb 55%,#1e40af);color:#fff;border-radius:32px;padding:28px 22px;margin-top:28px}} .how h2{{color:#fff}} .step{{display:flex;gap:16px;margin-top:24px}} .num{{width:52px;height:52px;background:#fff;color:#1e40af;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:22px;flex-shrink:0}} .step p{{color:#dbeafe}}
.testi{{background:#f0f7ff;border:1px solid #dbeafe;border-radius:22px;padding:18px;margin-top:14px}} .stars{{color:#f59e0b;font-size:20px;letter-spacing:3px}}
.faq{{background:#f0f7ff;border:1px solid #dbeafe;border-radius:20px;padding:16px;margin-top:12px}} .faq summary{{font-weight:800;cursor:pointer;display:flex;justify-content:space-between}}
.sticky{{position:fixed;left:0;right:0;bottom:0;background:#fff;border-top:1px solid #e2e8f0;padding:12px 14px;display:flex;align-items:center;justify-content:space-between;gap:12px;z-index:20}} .sticky .btn-blue{{height:48px;padding:0 18px;font-size:17px;flex-shrink:0;min-width:150px}}
</style></head><body>
<div class="top"><div class="logo"><a href="{MAIN_URL}" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:10px;text-decoration:none;color:#0f172a"><img src="../../logo.png"><span>Service<b style="color:#2563eb">App</b></span></a></div><div class="badge">Conta oficial ServiceApp</div></div>
<div class="wrap"><div class="card">
<div style="display:flex;gap:12px;align-items:flex-start"><a href="{MAIN_URL}" target="_blank" rel="noopener"><img src="../../logo.png" style="width:52px;height:52px;border-radius:50%;object-fit:cover"></a><div><b style="font-size:18px">ServiceApp</b><div style="color:#64748b;font-size:14px">Novo pedido de {service_pt} perto de voce</div></div><div style="color:#64748b;font-size:14px;margin-left:auto">agora</div></div>
<div class="pill">Projeto para aprovacao - <a href="{MAIN_URL}" target="_blank" rel="noopener" style="color:#1e40af">serviceapp.mobi</a></div>
<h1>{service_pl} em {city_name}</h1><p class="lead">Precisa de {service_pt} agora? Peca em 1 minuto, sem procura.</p>
<a class="btn-blue" href="{PLAY_LINK}" target="_blank" rel="noopener">Baixar gratis</a><p class="note">Sem assinatura. Sem comissao sobre o pedido.</p>
<div class="stores"><a class="store" href="{APPSTORE_LINK}" target="_blank" rel="noopener">A <small>Baixar para iPhone</small></a><a class="store" href="{PLAY_LINK}" target="_blank" rel="noopener">P <small>Baixar para Android</small></a></div>
<div style="text-align:center;color:#64748b;font-size:14px;margin-top:18px;border-top:1px solid #e2e8f0;padding-top:16px">Simples, rapido e sem compromisso - <a href="{MAIN_URL}" target="_blank" rel="noopener" style="color:#2563eb;font-weight:700">serviceapp.mobi</a></div></div>
<div style="margin-top:28px"><h2 style="font-size:32px">Sem procura. Sem espera desnecessaria.</h2>
<div class="mini"><div><b>Voce nao precisa procurar prestadores</b><p style="color:#64748b">O app faz isso por voce.</p></div></div>
<div class="mini"><div><b>Espera minima</b><p style="color:#64748b">Faca o pedido em 1 minuto e acompanhe a resposta.</p></div></div>
<div class="mini"><div><b>Contato imediato</b><p style="color:#64748b">Se o prestador aceitar, ele entra em contato imediatamente.</p></div></div></div>
<div class="how"><div style="color:#bae6fd;font-weight:800;letter-spacing:2px;font-size:13px">COMO FUNCIONA</div><h2 style="font-size:32px">Tres passos e pronto</h2>
<div class="step"><div class="num">1</div><div><h3>Baixe gratis</h3><p>Instale o ServiceApp no seu celular, sem custo. <a href="{PLAY_LINK}" target="_blank" rel="noopener" style="color:#fff;font-weight:700">Android</a> / <a href="{APPSTORE_LINK}" target="_blank" rel="noopener" style="color:#fff;font-weight:700">iPhone</a></p></div></div>
<div class="step"><div class="num">2</div><div><h3>Peca seu servico em 1 minuto</h3><p>Conte o que precisa, sem procurar prestador por prestador.</p></div></div>
<div class="step"><div class="num">3</div><div><h3>O prestador entra em contato imediatamente</h3><p>Ao aceitar o pedido, ele fala direto com voce.</p></div></div></div>
<div style="margin-top:28px"><div style="color:#2563eb;font-weight:800;letter-spacing:2px;font-size:13px">PARA PRESTADORES</div><h2 style="font-size:32px">Receba pedidos prontos para atender</h2><p style="color:#64748b">Voce recebe o pedido perto de voce, aceita em 1 clique e fala direto com o cliente.</p>
<div class="mini"><div><b>Pedidos perto de voce</b><p style="color:#64748b">Raio 2km, 5km ou 10km.</p></div></div>
<div class="mini"><div><b>Sem mensalidade para comecar</b><p style="color:#64748b">Taxa de aceitacao 29 BRL so quando voce aceita.</p></div></div>
<div class="mini"><div><b>Promocao para 10, 20, 50 ou 100 pessoas</b><p style="color:#64748b">1 BRL por pessoa. Push ou Push + SMS.</p></div></div></div>
<div style="margin-top:28px"><h2 style="font-size:32px">O que dizem em {city_name}</h2>
<div class="testi"><div class="stars">★★★★★</div><p>Nao precisei ficar procurando ninguem. Pedi pelo app, o prestador aceitou e me ligou na hora.</p><b>Joao</b> <span style="color:#64748b">{city_name}</span></div>
<div class="testi"><div class="stars">★★★★★</div><p>Pedi em 1 minuto. Em poucos minutos ja tinha resposta e fechei o servico.</p><b>Maria</b> <span style="color:#64748b">{city_name}</span></div></div>
<div style="margin-top:28px"><div style="color:#2563eb;font-weight:800;letter-spacing:2px;font-size:13px">PERGUNTAS FREQUENTES</div><h2 style="font-size:32px">Duvidas rapidas</h2>
<details class="faq" open><summary>Preciso pagar para baixar o app? <span>^</span></summary><p style="color:#64748b">Nao. O app e gratis para baixar e usar. <a href="{PLAY_LINK}" target="_blank" rel="noopener">Android</a> / <a href="{APPSTORE_LINK}" target="_blank" rel="noopener">iPhone</a></p></details>
<details class="faq"><summary>Preciso procurar os profissionais? <span>></span></summary><p style="color:#64748b">Nao. Voce cria o pedido e o app avisa os 10 prestadores mais proximos.</p></details>
<details class="faq"><summary>Em quanto tempo recebo o contato? <span>></span></summary><p style="color:#64748b">Assim que um prestador aceitar, ele entra em contato direto com voce.</p></details></div>
<div style="margin-top:28px;background:#fff;border:2px solid #2563eb;border-radius:20px;padding:20px">
<h3 style="color:#1e40af;margin:0 0 12px">Zobacz tez - {service_pl} w innych miastach</h3>
<div style="display:flex;flex-direction:column;gap:10px">{city_links}</div>
<h3 style="color:#1e40af;margin:20px 0 12px">Inne uslugi w {city_name}</h3>
<div style="display:flex;flex-direction:column;gap:10px">{service_links}</div>
<p style="margin-top:16px"><a href="../../" target="_blank" rel="noopener" style="color:#2563eb;font-weight:800">Wroc do Radar Panel ServiceApp</a></p>
<p><a href="{MAIN_URL}" target="_blank" rel="noopener" style="color:#2563eb;font-weight:800">serviceapp.mobi - Strona glowna</a></p>
<p><a href="{PLAY_LINK}" target="_blank" rel="noopener" style="color:#2563eb;font-weight:800">Pobierz dla Android</a></p>
<p><a href="{APPSTORE_LINK}" target="_blank" rel="noopener" style="color:#2563eb;font-weight:800">Pobierz dla iPhone</a></p>
</div>
<div style="text-align:center;padding:28px 0;color:#64748b"><div style="display:flex;align-items:center;justify-content:center;gap:10px;font-size:20px;font-weight:900;color:#0f172a"><a href="{MAIN_URL}" target="_blank" rel="noopener"><img src="../../logo.png" style="width:36px;height:36px;border-radius:8px;object-fit:cover"></a> Service<span style="color:#2563eb">App</span></div><p>Conta oficial ServiceApp</p><a href="{MAIN_URL}" target="_blank" rel="noopener" style="color:#1e40af;font-weight:800">serviceapp.mobi</a></div></div>
<div class="sticky"><div><b>{service_pl} em {city_name}</b><div style="color:#64748b;font-size:14px">Gratis - Pedido em 1 minuto - <a href="{MAIN_URL}" target="_blank" rel="noopener" style="color:#2563eb">serviceapp.mobi</a></div></div><a class="btn-blue" href="{PLAY_LINK}" target="_blank" rel="noopener">Baixar gratis</a></div>
</body></html>"""
    open(f"{path}/index.html", "w", encoding="utf-8").write(html)
    return f"landing/{slug}/"

pages = []
for pt, pl in SERVICES:
    for c_slug, c_name in CITIES:
        pages.append(make_page(pt, pl, c_slug, c_name))

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u in pages:
    sitemap += f"<url><loc>{u}</loc></url>\n"
sitemap += f"<url><loc>{MAIN_URL}/</loc></url>\n</urlset>"
open("_site/sitemap.xml", "w", encoding="utf-8").write(sitemap)
open("_site/robots.txt", "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nSitemap: sitemap.xml\n")
print(f"Created {len(pages)} landing pages")
