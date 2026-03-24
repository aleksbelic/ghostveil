from pathlib import Path
from src.ghostveil import encode, decode

img_dir_path = Path(__file__).parent / "img"
img_path = img_dir_path / "demo.png"
output_path = img_dir_path / "demo_output.png"

# Encode message into image
encode("Memento mori ut memineris vivere", img_path=img_path, output_path=output_path)

# Decode message from image
msg: str = decode(img_path=output_path)
print(msg)
