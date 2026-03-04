from PIL import Image
from pathlib import Path

src_dir_path = Path(__file__).parent
root_dir_path = src_dir_path.parent
img_dir_path = root_dir_path / "img"
img_path = img_dir_path / "demo_clean.png"

img = Image.open(img_path)

bw = img.convert("L")

output_path = img_dir_path / "demo_bw.png"
bw.save(output_path)
