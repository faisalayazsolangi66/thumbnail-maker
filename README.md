# Thumbnail Maker

Create thumbnails from images. Give it one image file or a folder of images and it writes a smaller thumbnail for each one, keeping the aspect ratio by default.

## Requirements

- Python 3
- Pillow (`pip install -r requirements.txt`)

## How to run

```bash
pip install -r requirements.txt
python3 main.py --help
python3 main.py photos/ --size 256x256 --output thumbnails/
```

Options:

- `--size WIDTHxHEIGHT` — max thumbnail size (default: `256x256`)
- `--output` — output folder (default: `thumbnails`)
- `--suffix` — suffix added before the extension (default: `_thumb`)
- `--exact` — pad thumbnails to the exact size instead of keeping the aspect ratio

## Example

```bash
$ python3 main.py photos/ --size 200x200 --output thumbs/
photos/sunset.jpg -> thumbs/sunset_thumb.jpg (200x133)
photos/cat.png -> thumbs/cat_thumb.png (200x200)
Done: 2 thumbnail(s) created, 0 failed.
```
