"""Convert bosskey_icon.png to bosskey.ico for Windows tray support."""
from PIL import Image
import sys
import os

def convert_png_to_ico(png_path: str, ico_path: str) -> None:
    img = Image.open(png_path).convert("RGBA")
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    resized = [img.resize(size, Image.LANCZOS) for size in sizes]
    resized[0].save(ico_path, format="ICO", sizes=sizes, append_images=resized[1:])
    print(f"Saved: {ico_path}")

if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    png = os.path.join(base, "bosskey_icon.png")
    ico = os.path.join(base, "bosskey.ico")
    convert_png_to_ico(png, ico)
