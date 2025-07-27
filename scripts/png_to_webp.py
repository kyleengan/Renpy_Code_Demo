import sys
from PIL import Image

def compress_image(source_path: str, webp_path: str, method: int):
    with Image.open(source_path) as img:
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        img.save(webp_path, method=method, quality=100)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python png_to_webp.py <image_path>")
        sys.exit(1)
    path = sys.argv[1]
    print(f"Processing {path}")
    compress_image(path, path[:-4] + ".webp", method=5)
    print("Image processed.")

else:
    print("No image path provided.")
    sys.exit(1)