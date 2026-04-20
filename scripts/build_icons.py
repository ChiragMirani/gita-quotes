"""Generate favicon, Apple touch icon, and PWA icons for Gita Quotes.

Design: warm cream background, saffron Om (ॐ) centered, "GITA" wordmark below.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


DOCS = Path(__file__).resolve().parents[1] / "docs"

BG = (250, 244, 232)        # warm cream
OM_COLOR = (255, 153, 51)   # India saffron
LABEL_COLOR = (74, 47, 24)  # dark warm brown


def find_font(path_options: list[str], size: int) -> ImageFont.FreeTypeFont:
    for path in path_options:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def devanagari_font(size: int) -> ImageFont.FreeTypeFont:
    return find_font([
        "C:/Windows/Fonts/Nirmala.ttc",
        "C:/Windows/Fonts/NirmalaB.ttf",
        "C:/Windows/Fonts/Mangal.ttf",
        "C:/Windows/Fonts/Aparajita.ttf",
        "/System/Library/Fonts/Supplemental/Devanagari MT.ttc",
        "/usr/share/fonts/truetype/lohit-devanagari/Lohit-Devanagari.ttf",
    ], size)


def label_font(size: int) -> ImageFont.FreeTypeFont:
    return find_font([
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ], size)


def render(size: int) -> Image.Image:
    img = Image.new("RGB", (size, size), BG)
    draw = ImageDraw.Draw(img)

    # Om symbol, large and centered in the upper portion. Bottom-anchor so the
    # full glyph (including the chandrabindu) always fits inside the canvas.
    om_size = int(size * 0.58)
    f_om = devanagari_font(om_size)
    om = "ॐ"
    bbox = draw.textbbox((0, 0), om, font=f_om)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (size - tw) // 2 - bbox[0]
    ty = int(size * 0.12) - bbox[1]
    draw.text((tx, ty), om, fill=OM_COLOR, font=f_om)

    # "GITA" wordmark below.
    label_size = max(8, int(size * 0.18))
    f_label = label_font(label_size)
    label = "GITA"
    bbox = draw.textbbox((0, 0), label, font=f_label)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (size - tw) // 2 - bbox[0]
    ty = int(size * 0.76) - bbox[1]
    draw.text((tx, ty), label, fill=LABEL_COLOR, font=f_label)

    return img


def main() -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    for name, size in [
        ("favicon-32.png", 32),
        ("favicon-192.png", 192),
        ("favicon-512.png", 512),
        ("apple-touch-icon.png", 180),
    ]:
        img = render(size)
        path = DOCS / name
        img.save(path, optimize=True)
        print(f"  wrote {path}  ({size}x{size})")
    base = render(64)
    base.save(DOCS / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print(f"  wrote {DOCS / 'favicon.ico'}  (multi-size)")


if __name__ == "__main__":
    main()
