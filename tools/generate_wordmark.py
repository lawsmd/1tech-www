"""Render the 1tech homepage wordmark to wordmark.png.

Run from the repo root:

    python tools/generate_wordmark.py

Produces wordmark.png at the repo root. The PNG is a transparent-background,
white-text rasterization of the 6-line ASCII wordmark from index.html, drawn
with Cascadia Mono so the output matches what desktop browsers currently render.

This script is a one-time build helper. Cloudflare Pages serves the resulting
PNG; it does not run this script. Re-run it locally if the wordmark text or
desired resolution changes, then commit the new wordmark.png.
"""

from pathlib import Path
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Pillow is required. Install with:  pip install Pillow")

REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT = REPO_ROOT / "wordmark.png"

FONT_CANDIDATES = [
    # Consolas tiles heavy-block and box-drawing glyphs flush with no
    # sub-pixel gaps — the result matches the look the desktop site has
    # always shown, but rendered once into an image instead of relying on
    # the visitor's font fallback.
    r"C:\Windows\Fonts\consola.ttf",
    r"C:\Windows\Fonts\lucon.ttf",
    r"C:\Windows\Fonts\cour.ttf",
    r"C:\Windows\Fonts\CascadiaMono.ttf",
]

FONT_SIZE = 80

WORDMARK_LINES = [
    " ██╗████████╗███████╗ ██████╗██╗  ██╗",
    "███║╚══██╔══╝██╔════╝██╔════╝██║  ██║",
    "╚██║   ██║   █████╗  ██║     ███████║",
    " ██║   ██║   ██╔══╝  ██║     ██╔══██║",
    " ██║   ██║   ███████╗╚██████╗██║  ██║",
    " ╚═╝   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝",
]


def pick_font() -> ImageFont.FreeTypeFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, FONT_SIZE)
    sys.exit(
        "No suitable monospace font found. Tried:\n  " + "\n  ".join(FONT_CANDIDATES)
    )


def render() -> Image.Image:
    font = pick_font()

    # Measure widest line so the canvas is wide enough.
    max_width = max(font.getbbox(line)[2] for line in WORDMARK_LINES)
    # Tight line height = font size, mimicking CSS line-height: 1.
    line_height = FONT_SIZE
    canvas_height = line_height * len(WORDMARK_LINES) + FONT_SIZE  # padding for descenders
    canvas_width = max_width + FONT_SIZE  # small horizontal padding

    img = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    for i, line in enumerate(WORDMARK_LINES):
        draw.text((FONT_SIZE // 2, i * line_height), line, font=font, fill=(255, 255, 255, 255))

    # Crop to the actual drawn pixels (alpha bbox).
    bbox = img.getbbox()
    if bbox is None:
        sys.exit("Rendered image was empty — check the font and ASCII content.")
    return img.crop(bbox)


def main() -> None:
    img = render()
    img.save(OUTPUT, format="PNG", optimize=True)
    size_kb = OUTPUT.stat().st_size / 1024
    print(f"Wrote {OUTPUT.relative_to(REPO_ROOT)}  {img.width}x{img.height}px  {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
