from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "vlctube.ico"


def build(size: int = 512) -> Image.Image:
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    scale = size / 512

    def box(values):
        return tuple(int(value * scale) for value in values)

    draw.rounded_rectangle(
        box((20, 20, 492, 492)),
        radius=int(108 * scale),
        fill=(5, 11, 20, 255),
        outline=(25, 126, 217, 255),
        width=max(2, int(6 * scale)),
    )
    draw.line(box((92, 132, 420, 132)), fill=(18, 59, 96, 220), width=max(3, int(10 * scale)))
    draw.line(box((92, 380, 420, 380)), fill=(18, 59, 96, 220), width=max(3, int(10 * scale)))

    triangle = [(194, 150), (194, 323), (371, 236)]
    draw.polygon([(int(x * scale), int(y * scale)) for x, y in triangle], fill=(43, 158, 239, 255))

    draw.arc(box((92, 204, 178, 308)), start=90, end=270, fill=(105, 220, 255, 255), width=max(3, int(18 * scale)))
    draw.arc(box((334, 204, 428, 308)), start=270, end=90, fill=(42, 152, 240, 255), width=max(3, int(18 * scale)))
    draw.rounded_rectangle(box((101, 411, 411, 429)), radius=int(9 * scale), fill=(104, 217, 255, 245))
    return image


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image = build()
    image.save(
        OUTPUT,
        format="ICO",
        sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)],
    )
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
