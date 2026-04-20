"""Generate favicon, Apple touch icon, and PWA icons for Gita Quotes."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


DOCS = Path(__file__).resolve().parents[1] / "docs"

BG = (26, 17, 8)        # deep brown / sepia
FG = (243, 234, 212)    # warm off-white
ACCENT = (232, 149, 86) # saffron / amber


def find_font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in candidates:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def render(size: int) -> Image.Image:
    img = Image.new("RGB", (size, size), BG)
    draw = ImageDraw.Draw(img)

    # Stylized arrow (Arjuna's bow shot) drawn as a clean diagonal with arrowhead.
    pad = size * 0.18
    x0, y0 = pad, size - pad * 0.9
    x1, y1 = size - pad, pad * 0.95
    line_w = max(2, int(size * 0.045))
    draw.line([(x0, y0), (x1, y1)], fill=ACCENT, width=line_w)
    # Arrowhead
    head = size * 0.13
    draw.polygon([
        (x1, y1),
        (x1 - head, y1 + head * 0.35),
        (x1 - head * 0.35, y1 + head),
    ], fill=ACCENT)

    # "BG" monogram lower-left
    font = find_font(int(size * 0.34))
    text = "BG"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = int(size * 0.10) - bbox[0]
    ty = int(size - th - size * 0.10) - bbox[1]
    draw.text((tx, ty), text, fill=FG, font=font)

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
