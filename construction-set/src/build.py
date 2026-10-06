"""Build: SVG sheets -> multi-page PDF (Chromium), per-sheet PNG previews, DXF, BOQ."""
import os, subprocess, sys, html
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
OUT = os.path.join(os.path.dirname(__file__), "..", "output")


def to_pdf(sheets, name):
    os.makedirs(OUT, exist_ok=True)
    pages = "\n".join(f'<div class="pg">{s.svg()}</div>' for s in sheets)
    doc = f"""<!doctype html><html><head><meta charset="utf-8"><style>
@page {{ size: 420mm 297mm; margin: 0 }}
html,body {{ margin:0; padding:0 }}
.pg {{ width:420mm; height:297mm; page-break-after: always; overflow:hidden }}
.pg:last-child {{ page-break-after: auto }}
svg {{ display:block }}
</style></head><body>{pages}</body></html>"""
    hp = os.path.abspath(os.path.join(OUT, name + ".html"))
    open(hp, "w").write(doc)
    pdf = os.path.abspath(os.path.join(OUT, name + ".pdf"))
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", "file://" + hp], check=True, capture_output=True)
    os.remove(hp)
    return pdf


def to_svgs(sheets, folder):
    d = os.path.join(OUT, folder)
    os.makedirs(d, exist_ok=True)
    for s in sheets:
        open(os.path.join(d, s.number + ".svg"), "w").write(s.svg())


def preview(sheet, path, scale=2):
    hp = os.path.abspath(path + ".html")
    open(hp, "w").write(f'<html><body style="margin:0">{sheet.svg()}</body></html>')
    w, h = int(420 * 3.78 * scale), int(297 * 3.78 * scale)
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    f"--force-device-scale-factor={scale}", f"--window-size={int(420*3.78)},{int(297*3.78)+90}",
                    f"--screenshot={os.path.abspath(path)}", "file://" + hp], check=True, capture_output=True)
    os.remove(hp)
