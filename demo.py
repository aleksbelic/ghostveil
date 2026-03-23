from pathlib import Path
from src.ghostveil import encode

img_dir_path = Path(__file__).parent / "img"

encode(
    "Memento mori ut memineris vivere",
    img_path=img_dir_path / "demo.png",
    output_path=img_dir_path / "demo_output.png",
)
