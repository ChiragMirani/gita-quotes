"""Generate a 1280x640 social-preview card for Gita Quotes."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / "docs" / "social-preview.png"

BG = (26, 17, 8)
FG = (243, 234, 212)
MUTED = (184, 167, 134)
ACCENT = (232, 149, 86)


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


def main() -> None:
    W, H = 1280, 640
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # Diagonal arrow accent across the bottom right
    pad = 80
    draw.line([(pad, H - pad), (W - pad, pad + 60)], fill=ACCENT, width=10)
    head = 50
    draw.polygon([
        (W - pad, pad + 60),
        (W - pad - head, pad + 60 + head * 0.35),
        (W - pad - head * 0.35, pad + 60 + head),
    ], fill=ACCENT)

    title = "Bhagavad Gita Quotes"
    sub   = "All 700 verses in English"
    sub2  = "Free to quote. Public-domain translation."
    by    = "by Chirag Mirani"

    f_title = find_font(96, bold=True)
    f_sub   = find_font(40, bold=False)
    f_sub2  = find_font(28, bold=False)
    f_by    = find_font(28, bold=True)

    draw.text((80, 110), title, fill=FG,    font=f_title)
    draw.text((80, 230), sub,   fill=FG,    font=f_sub)
    draw.text((80, 290), sub2,  fill=MUTED, font=f_sub2)
    draw.text((80, 360), by,    fill=ACCENT,font=f_by)

    img.save(OUT, optimize=True)
    print(f"Wrote {OUT}  ({W}x{H})")


if __name__ == "__main__":
    main()
