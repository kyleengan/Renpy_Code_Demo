import glob
from PIL import Image

def compress_image(source_path: str, webp_path: str, method: int):
    with Image.open(source_path) as img:
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        img.save(webp_path, method=method, quality=100)


file_list = glob.glob('game/images/**/*.png', recursive=True)

for path in file_list:
    print(f"Processing {path}")
    compress_image(path, path[:-4] + ".webp", method=4)