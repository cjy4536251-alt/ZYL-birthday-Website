from pathlib import Path
import io
import re
import subprocess

import imageio_ffmpeg
from PIL import Image


root = Path(__file__).parent
dist = root / "birthday-site" / "dist"
html = (dist / "index.html").read_text(encoding="utf-8")

# Keep photos crisp enough for a phone while reducing the initial HTML transfer.
cache = {}
pattern = re.compile(r"data:image/webp;base64,([A-Za-z0-9+/=]+)")


def compact_image(match):
    import base64

    original = match.group(1)
    if original in cache:
        return cache[original]
    image = Image.open(io.BytesIO(base64.b64decode(original)))
    if image.width > 1200:
        image.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
    output = io.BytesIO()
    image.save(output, format="WEBP", quality=72, method=6)
    replacement = "data:image/webp;base64," + base64.b64encode(output.getvalue()).decode()
    cache[original] = replacement
    return replacement


html = pattern.sub(compact_image, html)

for name in ("cake-real", "candle-real"):
    image = Image.open(dist / f"{name}.png")
    image.save(dist / f"{name}.webp", format="WEBP", quality=78, method=6)
    html = html.replace(f"{name}.png", f"{name}.webp")

audio = dist / "music.mp3"
if not audio.exists():
    subprocess.run(
        [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-i", str(dist / "music.flac"),
         "-codec:a", "libmp3lame", "-b:a", "96k", str(audio)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
html = html.replace("music.flac", "music.mp3")

(dist / "index.html").write_text(html, encoding="utf-8")
(root / "index.html").write_text(html, encoding="utf-8")
for name in ("cake-real.webp", "candle-real.webp", "music.mp3"):
    (root / name).write_bytes((dist / name).read_bytes())

print("HTML:", len(html.encode()), "bytes")
for name in ("cake-real.webp", "candle-real.webp", "music.mp3"):
    print(name, (dist / name).stat().st_size, "bytes")
