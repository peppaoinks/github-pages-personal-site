#!/usr/bin/env python3
"""Create oriented, metadata-free WebP derivatives; never modify source media."""
import argparse
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sources", type=Path, nargs="+")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--max-edge", type=int, default=1200)
    parser.add_argument("--quality", type=int, default=78)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    if args.max_edge < 1 or not 1 <= args.quality <= 100:
        parser.error("max-edge must be positive and quality must be 1..100")
    try:
        from PIL import Image, ImageOps
    except ImportError:
        parser.error("Pillow is required: python3 -m pip install Pillow")
    try:
        from pillow_heif import register_heif_opener
        register_heif_opener()
    except ImportError:
        pass
    sources = [p.resolve() for p in args.sources]
    outputs = [(args.output_dir / (p.stem + ".webp")).resolve() for p in sources]
    if len(set(outputs)) != len(outputs):
        parser.error("source stems collide; rename derivatives or process separately")
    for source, output in zip(sources, outputs):
        if not source.is_file():
            parser.error(f"source does not exist: {source.name}")
        if output in sources:
            parser.error("output would overwrite source media")
        if output.exists() and not args.overwrite:
            parser.error(f"output exists: {output.name}; use --overwrite for derivatives")
    if args.report:
        report = args.report.resolve()
        if report in sources or report in outputs:
            parser.error("report must not overwrite source media or an output image")
        if report.exists() and not args.overwrite:
            parser.error("report exists; choose another path or use --overwrite")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for source, output in zip(sources, outputs):
        with Image.open(source) as image:
            if getattr(image, "n_frames", 1) != 1:
                raise ValueError(f"animated/multi-frame input needs a separate workflow: {source.name}")
            exif = image.getexif()
            try:
                exif_ifd = exif.get_ifd(34665)
            except (AttributeError, KeyError, TypeError):
                exif_ifd = {}
            captured = exif_ifd.get(36867) or exif.get(36867)
            original_size = list(image.size)
            orientation = exif.get(274)
            oriented = ImageOps.exif_transpose(image)
            oriented.thumbnail((args.max_edge, args.max_edge), Image.Resampling.LANCZOS)
            mode = "RGBA" if "A" in oriented.getbands() or "transparency" in oriented.info else "RGB"
            converted = oriented.convert(mode)
            clean = Image.frombytes(mode, converted.size, converted.tobytes())
            clean.save(output, "WEBP", quality=args.quality, method=6)
        records.append({
            "source": source.name, "output": output.name,
            "source_dimensions": original_size, "dimensions": list(clean.size),
            "source_orientation": orientation,
            "source_datetime_original": str(captured) if captured else None,
            "date_status": "needs_confirmation" if captured else "unknown",
            "source_bytes": source.stat().st_size, "output_bytes": output.stat().st_size,
        })
        print(f"{output.name}: {clean.width}x{clean.height}, {output.stat().st_size} bytes")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("Wrote local metadata report; confirm dates before publishing.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"Image conversion failed: {error}", file=sys.stderr)
        sys.exit(1)
