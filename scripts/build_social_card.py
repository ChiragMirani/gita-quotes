"""Generate a 1280x640 social-preview card for Gita Quotes."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / "docs" / "social-preview.png"

BG = (250, 244, 232)
OM_COLOR = (255, 153, 51)
TITLE_COLOR = (29, 29, 31)
MUTED = (110, 110, 115)


def find_font(paths: list[str], size: int) -> ImageFont.FreeTypeFont:
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


def deva(size: int) -> ImageFont.FreeTypeFont:
    return find_font([
        "C:/Windows/Fonts/Nirmala.ttc",
        "C:/Windows/Fonts/Mangal.ttf",
        "/System/Library/Fonts/Supplemental/Devanagari MT.ttc",
        "/usr/share/fonts/truetype/lohit-devanagari/Lohit-Devanagari.ttf",
    ], size)


def sans(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return find_font([
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ], size)


def main() -> None:
    W, H = 1280, 640
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Big Om mark on the right side.
    f_om = deva(440)
    om = "ॐ"
    bbox = draw.textbbox((0, 0), om, font=f_om)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    ox = W - tw - 100 - bbox[0]
    oy = (H - th) // 2 - bbox[1] - 20
    draw.text((ox, oy), om, fill=OM_COLOR, font=f_om)

    # Title block on the left.
    title = "Bhagavad Gita"
    line2 = "Quotes"
    sub   = "All 700 verses in English"
    sub2  = "Free to quote. Public-domain translation."
    by    = "by Chirag Mirani"

    f_title = sans(96, bold=True)
    f_sub   = sans(36, bold=False)
    f_sub2  = sans(26, bold=False)
    f_by    = sans(26, bold=True)

    draw.text((80, 110), title, fill=TITLE_COLOR, font=f_title)
    draw.text((80, 215), line2, fill=TITLE_COLOR, font=f_title)
    draw.text((80, 360), sub,   fill=TITLE_COLOR, font=f_sub)
    draw.text((80, 415), sub2,  fill=MUTED,       font=f_sub2)
    draw.text((80, 480), by,    fill=OM_COLOR,    font=f_by)

    img.save(OUT, optimize=True)
    print(f"Wrote {OUT}  ({W}x{H})")


if __name__ == "__main__":
    main()
