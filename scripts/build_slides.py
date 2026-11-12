"""Erzeugt docs/slides/ff-altenhammer-vorlage.pptx: 8 Folienlayouts (Neue Folie > Layout) plus Beispielfolien.
Aufruf: python scripts/build_template.py"""
import copy
from lxml import etree
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor as C
from pptx.enum.shapes import MSO_SHAPE

RED, GOLD, DARK, SURF, WHITE = "CC0000", "F0A500", "14284B", "F8F8F8", "FFFFFF"
H, B = "Oswald", "Inter"
NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')
W, HT = 13.333, 7.5
E = lambda v: int(v * 914400)

prs = Presentation(); prs.slide_width, prs.slide_height = Inches(W), Inches(HT)
scratch = Presentation(); scratch.slide_width, scratch.slide_height = prs.slide_width, prs.slide_height
_uid = [100]

def deco(layout, x, y, w, h, color, text=None, size=14, font=H, align="r", shadow=True):
    """Dekoratives Rechteck oder festen Text (z.B. Marke) ins Layout."""
    s = scratch.slides.add_slide(scratch.slide_layouts[6])
    if text:
        sh = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        r = sh.text_frame.paragraphs[0].add_run(); r.text = text
        r.font.size, r.font.name, r.font.bold = Pt(size), font, True; r.font.color.rgb = C.from_string(color)
        sh.text_frame.paragraphs[0].alignment = {"r": 3, "l": 1}[align]
    else:
        sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        sh.fill.solid(); sh.fill.fore_color.rgb = C.from_string(color); sh.line.fill.background()
        if not shadow: sh.shadow.inherit = False; sh._element.remove(sh._element.find("{http://schemas.openxmlformats.org/presentationml/2006/main}style"))
    _uid[0] += 1; sh._element.nvSpPr.cNvPr.set("id", str(_uid[0]))
    layout.shapes._spTree.append(copy.deepcopy(sh._element))

def ph(layout, typ, idx, name, x, y, w, h, size, color, font, bold=False, bullets=False, anchor="t", prompt="Text", upper=False):
    _uid[0] += 1
    ppr = ('<a:lvl1pPr marL="342900" indent="-342900" algn="l"><a:buFont typeface="Arial"/><a:buChar char="&#8226;"/>' if bullets
           else '<a:lvl1pPr marL="0" indent="0" algn="l"><a:buNone/>')
    pic = typ == "pic"
    body = ('<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="de-DE"/></a:p></p:txBody>' if pic else
            f'<p:txBody><a:bodyPr anchor="{anchor}"><a:normAutofit/></a:bodyPr><a:lstStyle>{ppr}'
            f'<a:spcAft><a:spcPts val="1000"/></a:spcAft>'
            f'<a:defRPr sz="{size*100}" b="{int(bold)}"{" cap=\"all\"" if upper else ""}><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="{font}"/></a:defRPr></a:lvl1pPr></a:lstStyle>'
            f'<a:p><a:r><a:rPr lang="de-DE"/><a:t>{prompt}</a:t></a:r></a:p></p:txBody>')
    phattr = f'type="{typ}"' + ("" if typ == "title" else f' idx="{idx}"')
    if typ == "body": phattr = f'idx="{idx}"'
    xml = (f'<p:sp {NS}><p:nvSpPr><p:cNvPr id="{_uid[0]}" name="{name}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
           f'<p:nvPr><p:ph {phattr}/></p:nvPr></p:nvSpPr><p:spPr><a:xfrm><a:off x="{E(x)}" y="{E(y)}"/>'
           f'<a:ext cx="{E(w)}" cy="{E(h)}"/></a:xfrm>'
           f'{"<a:prstGeom prst=\"rect\"><a:avLst/></a:prstGeom><a:solidFill><a:srgbClr val=\"E5E5E5\"/></a:solidFill>" if pic else ""}</p:spPr>{body}</p:sp>')
    layout.shapes._spTree.append(etree.fromstring(xml))

def setup(i, name, bgcolor):
    global layout
    layout = prs.slide_layouts[i]; layout.name = name
    tree = layout.shapes._spTree
    for el in list(tree)[2:]: tree.remove(el)  # Standard-Platzhalter entfernen
    layout.background.fill.solid(); layout.background.fill.fore_color.rgb = C.from_string(bgcolor)

def content_frame(title="Überschrift"):
    deco(layout, 0, 0, W, 0.12, RED)
    ph(layout, "title", 0, "Titel", 0.6, 0.45, 8.0, 0.95, 34, DARK, H, True, anchor="ctr", prompt=title, upper=True)

def foot(color): pass  # Fußzeile bewusst leer

# 1 Titel
setup(0, "FF Titel", DARK)
deco(layout, 0, 0, 0.35, HT, RED); deco(layout, 0.35, 0, 0.08, HT, GOLD)
ph(layout, "ctrTitle", 0, "Titel", 1.2, 1.8, 10.5, 2.3, 54, WHITE, H, True, anchor="b", prompt="Titel der Präsentation", upper=True)
ph(layout, "subTitle", 1, "Untertitel", 1.2, 4.6, 10.5, 1.6, 22, "CCCCCC", B, prompt="Untertitel · Name · Datum")
foot(GOLD)

# 2 Abschnitt
setup(1, "FF Abschnitt", RED)
deco(layout, 0, 0, W, 0.12, GOLD)
ph(layout, "title", 0, "Titel", 0.9, 2.2, 11, 1.6, 48, WHITE, H, True, anchor="b", prompt="Abschnittstitel", upper=True)
ph(layout, "body", 1, "Beschreibung", 0.9, 3.95, 11, 1.0, 22, WHITE, B, prompt="Kurzbeschreibung")

# 3 Aufzählung
setup(2, "FF Titel und Inhalt", SURF); content_frame(); foot("6B6B6B")
ph(layout, "body", 1, "Inhalt", 0.6, 1.9, 12.1, 4.8, 26, DARK, B, bullets=True, prompt="Erster Punkt")

# 4 Bild und Text
setup(3, "FF Bild und Text", SURF); content_frame(); foot("6B6B6B")
deco(layout, 0.6, 1.9, 5.6, 4.8, "E5E5E5")  # kein pic-Platzhalter: Keynote verwirft ihn
ph(layout, "body", 1, "Text", 6.8, 1.9, 5.9, 4.8, 22, DARK, B, bullets=True, prompt="Kernaussage zum Bild")

# 5 Zwei Spalten
setup(4, "FF Zwei Spalten", SURF); content_frame(); foot("6B6B6B")
for k, (x, col, nm) in enumerate([(0.6, RED, "Links"), (6.9, DARK, "Rechts")]):
    deco(layout, x, 1.9, 5.8, 0.6, col); deco(layout, x, 2.5, 5.8, 4.1, WHITE)
    ph(layout, "body", 1 + 2 * k, f"Kopf {nm}", x + 0.2, 1.9, 5.4, 0.6, 20, WHITE, H, True, anchor="ctr", prompt=f"Spalte {nm.lower()}", upper=True)
    ph(layout, "body", 2 + 2 * k, f"Inhalt {nm}", x + 0.25, 2.7, 5.3, 3.8, 20, DARK, B, bullets=True, prompt="Punkt eins")

# 6 Zitat
setup(5, "FF Zitat", DARK)
deco(layout, 0, 0, W, 0.12, RED)
deco(layout, 1.5, 0.0, 3, 2.0, GOLD, "„", 200)
ph(layout, "title", 0, "Zitat", 1.6, 3.2, 10.2, 2.0, 42, WHITE, H, True, anchor="ctr", prompt="Eine Aussage oder ein Merksatz.")
ph(layout, "body", 1, "Quelle", 1.6, 5.4, 9, 0.6, 18, "CCCCCC", B, prompt="Quelle · Name")
foot("AAAAAA")

# 7 Agenda
setup(6, "FF Agenda", SURF); content_frame("Agenda"); foot("6B6B6B")
for i in range(4):
    y = 1.9 + i * 1.25
    deco(layout, 0.6, y + 0.1, 1.8, 0.9, RED, f"{i+1:02d}", 48, align="l")
    ph(layout, "body", 1 + i, f"Punkt {i+1}", 2.5, y, 7.5, 1.05, 28, DARK, B, anchor="ctr", prompt="Punkt")
    ph(layout, "body", 5 + i, f"Zeit {i+1}", 10.2, y, 2.5, 1.05, 24, "6B6B6B", B, anchor="ctr", prompt="19:00")
    if i < 3: deco(layout, 0.6, y + 1.15, 12.1, 0.02, "D0D0D0", shadow=False)

# 8 Abschluss
setup(7, "FF Abschluss", DARK)
deco(layout, 0, HT - 0.35, W, 0.35, RED); deco(layout, 0, HT - 0.43, W, 0.08, GOLD)
ph(layout, "title", 0, "Titel", 1.0, 1.2, 11, 1.3, 60, WHITE, H, True, anchor="b", prompt="Vielen Dank", upper=True)
ph(layout, "body", 1, "Kontakt", 1.0, 3.0, 11, 2.8, 24, "DDDDDD", B, prompt="Name · Funktion")

for l in list(prs.slide_layouts)[8:]: prs.slide_layouts.remove(l)

# Beispielfolien: (Layout, {Platzhalter-idx: Text oder Liste})
EX = [
 (0, {0: "Titel der Präsentation", 1: ["Untertitel oder Anlass", "Name · Datum"]}),
 (1, {0: "Abschnittstitel", 1: "Kurzbeschreibung des Abschnitts"}),
 (2, {0: "Überschrift", 1: ["Erster Punkt, kurz und klar", "Zweiter Punkt", "Dritter Punkt"]}),
 (3, {0: "Bild und Text", 1: ["Kernaussage zum Bild", "Ort, Datum, Beteiligte"]}),
 (4, {0: "Zwei Spalten", 1: "Spalte links", 2: ["Punkt eins", "Punkt zwei"], 3: "Spalte rechts", 4: ["Punkt eins", "Punkt zwei"]}),
 (5, {0: "Eine Aussage oder ein Merksatz, der hängen bleibt.", 1: "Quelle · Name"}),
 (6, {0: "Agenda", 1: "Begrüßung", 2: "Berichte", 3: "Pause", 4: "Ausblick & Termine", 5: "19:00", 6: "19:15", 7: "20:00", 8: "20:15"}),
 (7, {0: "Vielen Dank", 1: ["Name · Funktion", "E-Mail · Telefon", "feuerwehr.altenhammer.bayern"]}),
]
for li, content in EX:
    s = prs.slides.add_slide(prs.slide_layouts[li])
    for idx, val in content.items():
        p = s.placeholders[idx]
        if isinstance(val, str) and val.endswith(".jpg"): p.insert_picture(val)  # beschneidet statt zu verzerren
        else:
            lines = val if isinstance(val, list) else [val]
            p.text_frame.text = lines[0]
            for l in lines[1:]: p.text_frame.add_paragraph().text = l
pic = prs.slides[3].shapes.add_picture("static/images/mannschaft.jpg", Inches(0.6), Inches(1.9))
r = 5.6 / 4.8; ar = pic.width / pic.height  # zuschneiden statt verzerren
if ar > r: c = (1 - r / ar) / 2; pic.crop_left = pic.crop_right = c
else: c = (1 - ar / r) / 2; pic.crop_top = pic.crop_bottom = c
pic.left, pic.top, pic.width, pic.height = Inches(0.6), Inches(1.9), Inches(5.6), Inches(4.8)
prs.save("docs/slides/ff-altenhammer-vorlage.pptx")
print([l.name for l in prs.slide_layouts], len(prs.slides._sldIdLst))
