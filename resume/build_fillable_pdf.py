"""Builds the fillable one-page PDF draft of the résumé from resume_data.json.

Details not yet supplied are rendered as editable AcroForm text fields so the
draft can be completed in any PDF viewer. Usage: python3 resume/build_fillable_pdf.py
"""
import json
import os

from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Joseph_Mmanuel_Castillo_Resume_Fillable_Draft.pdf")

with open(os.path.join(HERE, "resume_data.json"), encoding="utf-8") as fh:
    data = json.load(fh)

NAVY = HexColor("#1F3A5F")
GREY = HexColor("#555555")
FIELD_BG = HexColor("#FFF7CC")
FIELD_BORDER = HexColor("#C9B458")

PAGE_W, PAGE_H = A4
MARGIN = 20 * mm
CONTENT_W = PAGE_W - 2 * MARGIN
BODY_SIZE = 10.5
LEADING = 14

c = canvas.Canvas(OUT, pagesize=A4)
c.setTitle("Résumé - " + data["name"] + " (fillable draft)")
c.setAuthor(data["name"])
form = c.acroForm

y = PAGE_H - MARGIN


def text_field(name, x, y_baseline, width, value="", tooltip="", height=13, size=BODY_SIZE):
    """Draw the supplied value as plain text, or an editable field when it is missing."""
    if value:
        c.setFillColor(black)
        c.setFont("Helvetica", size)
        c.drawString(x, y_baseline, value)
        return
    form.textfield(
        name=name, tooltip=tooltip or name, value=value,
        x=x, y=y_baseline - 3.5, width=width, height=height,
        fontName="Helvetica", fontSize=size, textColor=black,
        fillColor=FIELD_BG, borderColor=FIELD_BORDER, borderWidth=0.5,
        forceBorder=True, fieldFlags="doNotScroll",
    )


def heading(title):
    global y
    y -= 16
    c.setFillColor(NAVY)
    c.setFont("Helvetica-Bold", 10.5)
    c.drawString(MARGIN, y, title.upper())
    y -= 4
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.8)
    c.line(MARGIN, y, PAGE_W - MARGIN, y)
    y -= LEADING


def paragraph(text, x=MARGIN, width=CONTENT_W, font="Helvetica", size=BODY_SIZE):
    global y
    c.setFillColor(black)
    c.setFont(font, size)
    for line in simpleSplit(text, font, size, width):
        c.drawString(x, y, line)
        y -= LEADING


def bullet(text):
    global y
    c.setFillColor(black)
    c.setFont("Helvetica", BODY_SIZE)
    c.drawString(MARGIN + 4, y, "•")
    paragraph(text, x=MARGIN + 14, width=CONTENT_W - 14)


# ---- Header -----------------------------------------------------------------
c.setFillColor(NAVY)
c.setFont("Helvetica-Bold", 20)
c.drawCentredString(PAGE_W / 2, y - 6, data["name"])
y -= 24
c.setFillColor(GREY)
c.setFont("Helvetica", 11)
c.drawCentredString(PAGE_W / 2, y, data["headline"])
y -= 20

# Contact line: email (fixed) + phone and location fields
c.setFillColor(black)
c.setFont("Helvetica", BODY_SIZE)
email_txt = "Email: " + data["email"]
phone_lbl = data["contact_fields"]["phone"]["label"] + ": "
loc_lbl = data["contact_fields"]["location"]["label"] + ": "
gap = 12
phone_val = data["contact_fields"]["phone"].get("value", "")
loc_val = data["contact_fields"]["location"].get("value", "")
phone_w = c.stringWidth(phone_val, "Helvetica", BODY_SIZE) if phone_val else 110
loc_w = c.stringWidth(loc_val, "Helvetica", BODY_SIZE) if loc_val else 110
total = (c.stringWidth(email_txt, "Helvetica", BODY_SIZE) + gap
         + c.stringWidth(phone_lbl, "Helvetica", BODY_SIZE) + phone_w + gap
         + c.stringWidth(loc_lbl, "Helvetica", BODY_SIZE) + loc_w)
x = (PAGE_W - total) / 2
c.drawString(x, y, email_txt)
x += c.stringWidth(email_txt, "Helvetica", BODY_SIZE) + gap
c.drawString(x, y, phone_lbl)
x += c.stringWidth(phone_lbl, "Helvetica", BODY_SIZE)
text_field("phone", x, y, phone_w, value=data["contact_fields"]["phone"].get("value", ""),
           tooltip=data["contact_fields"]["phone"]["placeholder"])
x += phone_w + gap
c.drawString(x, y, loc_lbl)
x += c.stringWidth(loc_lbl, "Helvetica", BODY_SIZE)
text_field("location", x, y, loc_w, value=data["contact_fields"]["location"].get("value", ""),
           tooltip=data["contact_fields"]["location"]["placeholder"])
y -= 10
c.setStrokeColor(NAVY)
c.setLineWidth(1.2)
c.line(MARGIN, y, PAGE_W - MARGIN, y)

# ---- Profile -----------------------------------------------------------------
heading("Profile")
paragraph(data["profile"])

# ---- Education ---------------------------------------------------------------
ed = data["education"]
heading("Education")
c.setFillColor(black)
c.setFont("Helvetica-Bold", BODY_SIZE)
c.drawString(MARGIN, y, ed["institution"])
lbl = ed["completion_label"] + ": "
date_w = 95
c.setFont("Helvetica", BODY_SIZE)
c.setFillColor(GREY)
lx = PAGE_W - MARGIN - date_w - c.stringWidth(lbl, "Helvetica", BODY_SIZE)
inst_w = c.stringWidth(ed["institution"], "Helvetica-Bold", BODY_SIZE)
if MARGIN + inst_w + 12 > lx:
    # Long institution name: move the completion date to its own line.
    y -= LEADING
c.drawString(lx, y, lbl)
text_field("academic_completion_date", PAGE_W - MARGIN - date_w, y, date_w,
           value=ed.get("completion_value", ""), tooltip=ed["completion_placeholder"])
y -= LEADING
paragraph(ed["degree"], font="Helvetica-Oblique")
for n in ed["notes"]:
    bullet(n)

# ---- Training and documents --------------------------------------------------
heading("Training and Documents")
for t in data["training_documents"]:
    bullet(t)

# ---- Sea service -------------------------------------------------------------
heading("Sea Service")
for t in data["sea_service"]:
    bullet(t)

# ---- Personal details --------------------------------------------------------
heading("Personal Details")
label_w = 95
for f in data["personal_fields"]:
    c.setFillColor(GREY)
    c.setFont("Helvetica-Bold", BODY_SIZE)
    c.drawString(MARGIN, y, f["label"])
    text_field(f["key"], MARGIN + label_w, y, CONTENT_W - label_w, value=f.get("value", ""),
               tooltip=f["placeholder"])
    y -= LEADING + 4

# ---- Footer ------------------------------------------------------------------
y -= 10
c.setFillColor(GREY)
c.setFont("Helvetica-Oblique", 8.5)
c.drawCentredString(PAGE_W / 2, y, data["footer"])

missing = (not data["contact_fields"]["phone"].get("value") or not data["contact_fields"]["location"].get("value")
           or not ed.get("completion_value") or any(not f.get("value") for f in data["personal_fields"]))
if missing:
    c.setFillColor(HexColor("#999999"))
    c.setFont("Helvetica", 7.5)
    c.drawCentredString(PAGE_W / 2, MARGIN / 2,
                        "DRAFT - shaded fields are editable. Complete all fields before sending; "
                        "do not attach this draft to applications.")

c.showPage()
c.save()
print("Wrote", OUT)
