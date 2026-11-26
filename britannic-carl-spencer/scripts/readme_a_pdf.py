#!/usr/bin/env python3
"""Convierte README.md / README.en.md en PDF con Chrome sin interfaz.

Uso:  python3 scripts/readme_a_pdf.py README.md Estudio_Britannic_Carl_Spencer.pdf
      python3 scripts/readme_a_pdf.py README.en.md Britannic_Carl_Spencer_Study.pdf

- Quita del PDF la línea que enlaza al propio PDF y los diagramas Mermaid
  (GitHub los dibuja en la web; en papel no hacen falta).
- Requiere pandoc y google-chrome.
"""
import os, re, subprocess, sys, tempfile

SRC, OUT = sys.argv[1], sys.argv[2]
BASE = os.path.dirname(os.path.abspath(SRC))
md = open(SRC, encoding="utf-8").read()
md = re.sub(r"^> 📄 .*\n", "", md, flags=re.M)                 # enlace al PDF
md = re.sub(r"```mermaid\n.*?```\n", "", md, flags=re.S)        # diagramas Mermaid
md = re.sub(r"<p align=\"right\">.*?</p>\n", "", md)              # «volver arriba»
# Fotos de Wikimedia: en el PDF se sustituyen por una nota (la web las muestra)
md = re.sub(r"<p align=\"center\">\s*<img[^>]*>.*?</p>\n", "> 🖼️ *Foto disponible en la versión web (GitHub).* / *Photo available in the web version (GitHub).*\n", md, flags=re.S)
title = re.sub(r"[^\w\sÀ-ÿ,().–-]", "", md.splitlines()[0].lstrip("# ")).strip()

CSS = """
@page { size: A4; margin: 18mm 17mm 18mm 17mm; }
body { font-family: 'DejaVu Sans', 'Noto Color Emoji', sans-serif; font-size: 9.6pt; line-height: 1.5; color: #1f2d3a; }
h1 { font-size: 21pt; color: #0b3d5c; margin: 0 0 4pt; }
h2 { font-size: 14pt; color: #0b3d5c; border-bottom: 1px solid #a9c3d3; padding-bottom: 3pt; margin-top: 18pt; break-after: avoid; }
h3 { font-size: 11pt; color: #1a5fa8; margin-top: 12pt; break-after: avoid; }
a { color: #1a5fa8; text-decoration: none; }
blockquote { margin: 8pt 0; padding: 5pt 10pt; background: #eaf3f8; border-left: 3px solid #0b3d5c; }
blockquote p { margin: 2pt 0; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 10pt; font-size: 7.9pt; page-break-inside: auto; }
tr { break-inside: avoid; }
th { background: #0b3d5c; color: #fff; text-align: left; padding: 4pt 5pt; }
td { padding: 3.5pt 5pt; border-bottom: 1px solid #d5e2ea; vertical-align: top; }
tr:nth-child(even) td { background: #f4f8fb; }
img { max-width: 100%; max-height: 210mm; display: block; margin: 6pt auto; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.5pt; }
hr { border: 0; border-top: 1px solid #d5e2ea; margin: 12pt 0; }
"""
with tempfile.TemporaryDirectory() as tmp:
    html = os.path.join(BASE, "_tmp_pdf.html")
    css = os.path.join(tmp, "s.css"); open(css, "w").write(CSS)
    mdtmp = os.path.join(tmp, "in.md"); open(mdtmp, "w", encoding="utf-8").write(md)
    subprocess.run(["pandoc", mdtmp, "-f", "gfm", "-t", "html5", "-s", "--metadata", f"title={title}",
                    "--css", css, "--embed-resources", "--resource-path", BASE, "-o", html], check=True)
    # pandoc añade un <header> con el título: se quita para no duplicarlo
    h = open(html, encoding="utf-8").read()
    h = re.sub(r"<header id=\"title-block-header\">.*?</header>", "", h, flags=re.S)
    open(html, "w", encoding="utf-8").write(h)
    try:
        subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
                        "--no-pdf-header-footer", "--virtual-time-budget=20000",
                        f"--print-to-pdf={os.path.abspath(OUT)}", "file://" + html],
                       check=True, capture_output=True)
    finally:
        os.remove(html)
print("PDF:", OUT)
