#!/usr/bin/env python3
"""Create thumbnails from images.

Reads one image file or every image in a folder and writes a smaller
thumbnail for each one, keeping the aspect ratio by default.
"""
import argparse
import os
import sys

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif", ".tiff"}


def parse_size(text):
    try:
        width, height = text.lower().replace("x", " ").split()
        width, height = int(width), int(height)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "size must look like WIDTHxHEIGHT, e.g. 256x256"
        )
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("size values must be positive")
    return width, height


def collect_images(path):
    if os.path.isfile(path):
        return [path]
    if os.path.isdir(path):
        found = []
        for name in sorted(os.listdir(path)):
            full = os.path.join(path, name)
            if os.path.isfile(full):
                if os.path.splitext(name)[1].lower() in IMAGE_EXTS:
                    found.append(full)
        return found
    return []


def make_thumbnail(src, dest, size, exact):
    from PIL import Image

    with Image.open(src) as image:
        if exact:
            thumb = image.copy()
            thumb.thumbnail(size)
            # Pad to the exact size on a white background.
            canvas = Image.new("RGB", size, (255, 255, 255))
            offset = ((size[0] - thumb.width) // 2,
                      (size[1] - thumb.height) // 2)
            canvas.paste(thumb.convert("RGB"), offset)
            canvas.save(dest)
            return canvas.size
        image.thumbnail(size)
        image.save(dest)
        return image.size


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Create thumbnails from images."
    )
    parser.add_argument("input", help="image file or folder of images")
    parser.add_argument("--size", type=parse_size, default=(256, 256),
                        help="max thumbnail size as WIDTHxHEIGHT (default: 256x256)")
    parser.add_argument("--output", default="thumbnails",
                        help="output folder (default: thumbnails)")
    parser.add_argument("--suffix", default="_thumb",
                        help="suffix added before the extension (default: _thumb)")
    parser.add_argument("--exact", action="store_true",
                        help="pad thumbnails to the exact size instead of keeping aspect ratio")
    args = parser.parse_args(argv)

    try:
        from PIL import Image  # noqa: F401  (checked early for a clear error)
    except ImportError:
        print("Error: Pillow is not installed. Install it with: pip install Pillow",
              file=sys.stderr)
        return 1

    images = collect_images(args.input)
    if not images:
        print(f"No images found in: {args.input}", file=sys.stderr)
        return 1

    os.makedirs(args.output, exist_ok=True)
    done, failed = 0, 0
    for src in images:
        stem, ext = os.path.splitext(os.path.basename(src))
        dest = os.path.join(args.output, f"{stem}{args.suffix}{ext}")
        try:
            new_size = make_thumbnail(src, dest, args.size, args.exact)
        except Exception as exc:
            print(f"Failed: {src}: {exc}", file=sys.stderr)
            failed += 1
            continue
        print(f"{src} -> {dest} ({new_size[0]}x{new_size[1]})")
        done += 1

    print(f"Done: {done} thumbnail(s) created, {failed} failed.")
    return 1 if failed and done == 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
