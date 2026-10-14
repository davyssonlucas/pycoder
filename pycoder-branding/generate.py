"""Generate pycoder branding assets (icons, splash, installer images).

Usage (from the repository root):
    python3 pycoder-branding/generate.py

Requires Pillow and the DejaVu fonts (fonts-dejavu-core on Debian/Ubuntu).
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
RESOURCES = ROOT / "python" / "resources"
IMAGES = ROOT / "python" / "build" / "images"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

# Release palette: blue -> teal. EAP palette: violet -> pink.
RELEASE = ("#2563EB", "#0D9488")
EAP = ("#7C3AED", "#DB2777")
ACCENT = "#FDE68A"
WHITE = "#FFFFFF"
SPLASH_BG = ("#0B1220", "#111C33")
MUTED = "#94A3B8"

SVG_TEMPLATE = """<svg width="{s}" height="{s}" viewBox="0 0 {s} {s}" fill="none" xmlns="http://www.w3.org/2000/svg">
<defs>
<linearGradient id="g" x1="0" y1="0" x2="{s}" y2="{s}" gradientUnits="userSpaceOnUse">
<stop stop-color="{c0}"/>
<stop offset="1" stop-color="{c1}"/>
</linearGradient>
</defs>
<rect width="{s}" height="{s}" rx="{rx}" fill="url(#g)"/>
<path d="M{ax} {ay}L{bx} {by}L{ax} {cy}" stroke="{white}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M{ux0} {cy}H{ux1}" stroke="{accent}" stroke-width="{sw}" stroke-linecap="round"/>
</svg>
"""

# Mark geometry in a 64-unit box: rounded square, white chevron, amber underscore.
GEOMETRY_64 = dict(s=64, rx=14, ax=18, ay=20, bx=32, by=32, cy=44, ux0=37, ux1=48, sw=6)
GEOMETRY_16 = dict(s=16, rx=3.5, ax=4.5, ay=5, bx=8, by=8, cy=11, ux0=9.5, ux1=12, sw=1.6)


def svg(geometry, palette):
  return SVG_TEMPLATE.format(c0=palette[0], c1=palette[1], white=WHITE, accent=ACCENT, **geometry)


def gradient(size, colors, diagonal=True):
  w, h = size
  c0 = Image.new("RGBA", size, colors[0])
  c1 = Image.new("RGBA", size, colors[1])
  mask = Image.new("L", size)
  px = mask.load()
  for y in range(h):
    for x in range(w):
      t = (x / max(w - 1, 1) + y / max(h - 1, 1)) / 2 if diagonal else y / max(h - 1, 1)
      px[x, y] = int(255 * t)
  return Image.composite(c1, c0, mask)


def stroke(draw, points, width, fill):
  draw.line(points, fill=fill, width=int(width), joint="curve")
  r = width / 2
  for x, y in (points[0], points[-1]):
    draw.ellipse((x - r, y - r, x + r, y + r), fill=fill)


def mark(size, palette=RELEASE):
  """Rasterize the 64-unit mark at `size` pixels, supersampled for smooth edges."""
  ss = 4
  big = size * ss
  k = big / 64
  g = GEOMETRY_64
  img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
  mask = Image.new("L", (big, big), 0)
  ImageDraw.Draw(mask).rounded_rectangle((0, 0, big - 1, big - 1), radius=g["rx"] * k, fill=255)
  img.paste(gradient((big, big), palette), (0, 0), mask)
  d = ImageDraw.Draw(img)
  stroke(d, [(g["ax"] * k, g["ay"] * k), (g["bx"] * k, g["by"] * k), (g["ax"] * k, g["cy"] * k)], g["sw"] * k, WHITE)
  stroke(d, [(g["ux0"] * k, g["cy"] * k), (g["ux1"] * k, g["cy"] * k)], g["sw"] * k, ACCENT)
  return img.resize((size, size), Image.LANCZOS)


def font(name, size):
  return ImageFont.truetype(str(FONT_DIR / name), size)


def splash(scale):
  w, h = 640 * scale, 400 * scale
  img = gradient((w, h), SPLASH_BG, diagonal=True)
  d = ImageDraw.Draw(img)
  icon = mark(88 * scale)
  img.alpha_composite(icon, (56 * scale, 96 * scale))
  d.text((164 * scale, 98 * scale), "pycoder", font=font("DejaVuSans-Bold.ttf", 58 * scale), fill=WHITE)
  d.text((168 * scale, 166 * scale), "Python IDE", font=font("DejaVuSans.ttf", 20 * scale), fill=MUTED)
  d.text((56 * scale, 330 * scale), "Built on the IntelliJ Platform Community Edition · Apache 2.0",
         font=font("DejaVuSans.ttf", 12 * scale), fill=MUTED)
  return img


def installer_sidebar(size):
  """Windows installer welcome image (portrait)."""
  w, h = size
  img = gradient(size, SPLASH_BG, diagonal=False)
  img.alpha_composite(mark(96), ((w - 96) // 2, 64))
  d = ImageDraw.Draw(img)
  f = font("DejaVuSans-Bold.ttf", 26)
  tw = d.textlength("pycoder", font=f)
  d.text(((w - tw) / 2, 180), "pycoder", font=f, fill=WHITE)
  return img.convert("RGB")


def installer_header(size):
  """Windows installer header strip (white background)."""
  w, h = size
  img = Image.new("RGBA", size, WHITE)
  img.alpha_composite(mark(41), (w - 41 - 8, (h - 41) // 2))
  ImageDraw.Draw(img).text((10, 16), "pycoder", font=font("DejaVuSans-Bold.ttf", 20), fill="#0B1220")
  return img.convert("RGB")


def dmg_background(size):
  w, h = size
  img = gradient(size, SPLASH_BG)
  d = ImageDraw.Draw(img)
  f = font("DejaVuSans.ttf", 13)
  text = "Drag pycoder to Applications"
  d.text(((w - d.textlength(text, font=f)) / 2, h - 40), text, font=f, fill=MUTED)
  return img


def main():
  for name, geometry, palette in [
    ("pycoder.svg", GEOMETRY_64, RELEASE),
    ("pycoder_16.svg", GEOMETRY_16, RELEASE),
    ("pycoder-eap.svg", GEOMETRY_64, EAP),
    ("pycoder-eap_16.svg", GEOMETRY_16, EAP),
  ]:
    (RESOURCES / name).write_text(svg(geometry, palette))

  splash(1).save(RESOURCES / "pycoder_logo.png")
  splash(2).save(RESOURCES / "pycoder_logo@2x.png")

  mark(128).save(IMAGES / "linux" / "product_128.png")
  mark(128, EAP).save(IMAGES / "linux" / "product_128_EAP.png")

  ico_sizes = [(16, 16), (20, 20), (24, 24), (32, 32), (40, 40), (48, 48), (64, 64), (256, 256)]
  mark(256).save(IMAGES / "win" / "product.ico", sizes=ico_sizes)
  mark(256, EAP).save(IMAGES / "win" / "product_EAP.ico", sizes=ico_sizes)
  small_ico = [(16, 16), (24, 24), (32, 32), (48, 48)]
  mark(48).save(IMAGES / "win" / "install.ico", sizes=small_ico)
  mark(48).save(IMAGES / "win" / "uninstall.ico", sizes=small_ico)
  installer_sidebar((164, 314)).save(IMAGES / "win" / "logo.bmp")
  installer_header((150, 57)).save(IMAGES / "win" / "headerlogo.bmp")

  mark(1024).save(IMAGES / "mac" / "product.icns")
  mark(1024, EAP).save(IMAGES / "mac" / "product_EAP.icns")
  dmg_background((455, 296)).save(IMAGES / "mac" / "dmg_background.tiff", compression="tiff_lzw")


if __name__ == "__main__":
  main()
