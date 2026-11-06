"""Build the profile's static SVG artwork from the original product marks."""

from html import escape
from base64 import b64encode
from pathlib import Path
from struct import unpack
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ET.register_namespace("", "http://www.w3.org/2000/svg")


def mark(name, x, y, width, height):
    png = ASSETS / "marks" / f"{name}.png"
    if png.exists():
        data = png.read_bytes()
        source_width, source_height = unpack(">II", data[16:24])
        encoded = b64encode(data).decode("ascii")
        return f'<svg x="{x}" y="{y}" width="{width}" height="{height}" viewBox="0 0 {source_width} {source_height}"><image width="{source_width}" height="{source_height}" href="data:image/png;base64,{encoded}"/></svg>'
    source = ET.parse(ASSETS / "marks" / f"{name}.svg").getroot()
    for node in list(source):
        if node.tag.endswith("title"):
            source.remove(node)
    content = "".join(ET.tostring(node, encoding="unicode") for node in source)
    return f'<svg x="{x}" y="{y}" width="{width}" height="{height}" viewBox="{source.attrib["viewBox"]}">{content}</svg>'


def text(x, y, value, size=24, color="#F1F3F5", weight=400, mono=False, **attrs):
    font = "ui-monospace, SFMono-Regular, Consolas, monospace" if mono else "Segoe UI, Arial, sans-serif"
    extra = " ".join(f'{key.replace("_", "-")}="{escape(str(value), quote=True)}"' for key, value in attrs.items())
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{color}" {extra}>{escape(value)}</text>'


def svg(name, height, title, body):
    artwork = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="{name}-title">
<title id="{name}-title">{escape(title)}</title>
{body}
</svg>
'''
    ET.fromstring(artwork)
    (ASSETS / f"{name}.svg").write_text(artwork, encoding="utf-8")


def profile():
    body = '''<defs>
  <pattern id="profile-grid" width="28" height="28" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#FFFFFF" fill-opacity=".07"/></pattern>
  <linearGradient id="profile-bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#111820"/><stop offset="1" stop-color="#0B0F15"/></linearGradient>
</defs>
<rect x="1" y="1" width="1198" height="398" rx="22" fill="url(#profile-bg)" stroke="#29323E"/>
<path d="M1 57H1199" stroke="#29323E"/>
<circle cx="29" cy="29" r="6" fill="#FF6B61"/><circle cx="51" cy="29" r="6" fill="#E9B75A"/><circle cx="73" cy="29" r="6" fill="#59BD88"/>
<rect x="821" y="75" width="347" height="292" rx="18" fill="url(#profile-grid)"/>
<path d="M906 166H1050V286H906Z" fill="none" stroke="#293849" stroke-width="2" stroke-dasharray="5 6"/>
'''
    body += text(108, 35, "~/marciosalinodias / README.md", 15, "#97A4B4", mono=True)
    body += text(49, 109, "IDEIAS → ARQUITETURA → PRODUTOS", 15, "#F48B50", mono=True, letter_spacing=2)
    body += text(46, 179, "Marcio Salino Dias", 58, weight=700, letter_spacing=-2)
    body += text(49, 222, "Tech Lead · Arquiteto de Software · IA", 26, "#C5CDD8")
    body += text(49, 272, "Da primeira decisão ao produto em produção.", 24, "#97A4B4")
    body += '<path d="M49 310H749" stroke="#29323E"/>'
    body += text(49, 354, "17+ anos em tecnologia", 21, "#E1E6EC", weight=600)
    body += text(355, 354, "Araranguá, SC · Brasil", 19, "#97A4B4")
    for x, y, color in [(851, 111, "#E66113"), (994, 111, "#8C00FF"), (922, 235, "#00B3FF")]:
        body += f'<rect x="{x}" y="{y}" width="112" height="106" rx="17" fill="#0E141D" stroke="{color}" stroke-opacity=".35"/>'
    body += mark("public-it", 869, 136, 76, 55)
    body += mark("handoff-it", 1001, 112, 98, 98)
    body += mark("ebook-se", 943, 253, 70, 70)
    body += mark("msd", 1091, 342, 83, 39)
    svg("profile", 400, "Marcio Salino Dias — arquitetura, IA e produtos. Mais de 17 anos em tecnologia.", body)


def product(name, color, tagline, category, url=None, display_name=None):
    label = display_name or name
    body = f'''<defs>
  <linearGradient id="{name}-bg" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#111820"/><stop offset="1" stop-color="#0B1017"/></linearGradient>
  <pattern id="{name}-grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{color}" stroke-opacity=".08"/></pattern>
</defs>
<rect x="1" y="1" width="1198" height="258" rx="21" fill="url(#{name}-bg)" stroke="#29323E"/>
<rect x="1" y="22" width="4" height="216" rx="2" fill="{color}"/>
<rect x="864" y="1" width="335" height="258" rx="21" fill="url(#{name}-grid)"/>
<rect x="942" y="39" width="181" height="181" rx="28" fill="#0E141D" stroke="{color}" stroke-opacity=".35"/>
'''
    body += text(43, 46, category, 15, color, mono=True, letter_spacing=1.5)
    body += text(40, 120, label, 68, weight=700, letter_spacing=-2)
    body += text(44, 170, tagline, 30, "#C3CDD9")
    body += text(44, 225, url or "CRIAÇÃO DE EBOOKS COM IA", 19, "#94A3B4", mono=True)
    body += mark(name, 955, 52, 155, 155)
    svg(name, 260, f"{label} — {tagline}", body)


profile()
product("public-it", "#E66113", "Sua IA cria. O public-it publica.", "PUBLICAÇÃO WEB", "public-it.com ↗")
product("handoff-it", "#A65CFF", "Troque de ferramenta. Continue de onde parou.", "CONTINUIDADE DE CONTEXTO", "handoff-it.com ↗")
product("ebook-se", "#00B3FF", "Da ideia ao ebook, com IA.", "CONTEÚDO E PUBLICAÇÃO", "ebook-fy.com ↗")
product("apexcode", "#8068FF", "Transformamos operações em sistemas inteligentes.", "ESTRATÉGIA, IA E SOFTWARE", "apexcode.digital ↗", display_name="ApexCode")
print("Generated profile.svg and four showcase cards.")
