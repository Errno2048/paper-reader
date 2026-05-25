#!/usr/bin/env python3
"""Extract PDF to Markdown with fallback strategies.

Usage:
    python extract_paper.py <pdf_path> [--output-dir <dir>]

Output:
    <output_dir>/paper.md     — full paper in Markdown
    <output_dir>/images/      — extracted embedded images

Stdout protocol:
    OK:<method>:<path>         — extraction succeeded
    WARN:<method>:<message>    — tier failed, falling back
    ERROR:<message>            — all methods failed
    ASK_USER:<message>         — human intervention needed
"""

import sys
import os
import argparse
from pathlib import Path


def extract_via_pymupdf4llm(pdf_path: str, output_dir: str) -> bool:
    """Tier 1: pymupdf4llm — best structural Markdown (headings, tables, math)."""
    import pymupdf4llm
    md_text = pymupdf4llm.to_markdown(pdf_path)
    out_path = os.path.join(output_dir, "paper.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md_text)
    return True


def extract_via_pymupdf_raw(pdf_path: str, output_dir: str) -> bool:
    """Tier 2: PyMuPDF raw text — always works, loses some structure."""
    import fitz
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        if text.strip():
            pages.append(f"## Page {i + 1}\n\n{text}")
    doc.close()

    if not pages:
        return False

    out_path = os.path.join(output_dir, "paper.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(pages))
    return True


def extract_images(pdf_path: str, output_dir: str) -> int:
    """Extract embedded images from PDF. Returns count of images extracted."""
    import fitz
    doc = fitz.open(pdf_path)
    img_dir = os.path.join(output_dir, "images")
    os.makedirs(img_dir, exist_ok=True)
    count = 0
    for page_num, page in enumerate(doc):
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
                ext = base_image["ext"]
                img_path = os.path.join(
                    img_dir, f"page{page_num + 1}_img{img_index + 1}.{ext}"
                )
                with open(img_path, "wb") as f:
                    f.write(base_image["image"])
                count += 1
            except Exception:
                continue
    doc.close()
    return count


def main():
    parser = argparse.ArgumentParser(
        description="Extract PDF to Markdown with fallback strategies"
    )
    parser.add_argument("pdf_path", help="Path to the PDF file")
    parser.add_argument(
        "--output-dir", "-o",
        default=None,
        help="Output directory (default: same directory as PDF)",
    )
    args = parser.parse_args()

    pdf_path = os.path.abspath(args.pdf_path)
    if not os.path.exists(pdf_path):
        print(f"ERROR:PDF file not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    output_dir = args.output_dir or os.path.dirname(pdf_path)
    output_parent = os.path.dirname(output_dir) if output_dir.endswith(
        os.sep) else output_dir
    # Use a subdirectory named after the PDF (without extension)
    if args.output_dir is None:
        base = os.path.splitext(os.path.basename(pdf_path))[0]
        output_dir = os.path.join(os.path.dirname(pdf_path), base)
    os.makedirs(output_dir, exist_ok=True)

    # Tier 1: pymupdf4llm
    try:
        extract_via_pymupdf4llm(pdf_path, output_dir)
        img_count = extract_images(pdf_path, output_dir)
        print(f"OK:pymupdf4llm:{output_dir}/paper.md")
        if img_count > 0:
            print(f"OK:images:{img_count} images extracted to {output_dir}/images/")
        return 0
    except ImportError:
        print("WARN:pymupdf4llm not installed, falling back to PyMuPDF raw text")
        print(
            "ASK_USER:pymupdf4llm is not installed. Install it for better Markdown "
            "quality (pip install pymupdf4llm), or continue with basic extraction? "
            "Reply 'install' to install, 'continue' to proceed with basic extraction."
        )
        # In automated context, fall through to Tier 2
    except Exception as e:
        print(f"WARN:pymupdf4llm failed: {e}, falling back to PyMuPDF raw text")

    # Tier 2: PyMuPDF raw text
    try:
        success = extract_via_pymupdf_raw(pdf_path, output_dir)
        if not success:
            print(
                "ERROR:PyMuPDF extracted no text. The PDF may be image-only or "
                "corrupted."
            )
            print(
                "ASK_USER:Please provide a Markdown or text version of this paper."
            )
            sys.exit(1)
        img_count = extract_images(pdf_path, output_dir)
        print(f"OK:pymupdf_raw:{output_dir}/paper.md")
        if img_count > 0:
            print(f"OK:images:{img_count} images extracted to {output_dir}/images/")
        return 0
    except ImportError:
        print("ERROR:PyMuPDF (fitz) is not installed.", file=sys.stderr)
        print(
            "ASK_USER:Neither pymupdf4llm nor PyMuPDF is available. "
            "Please install PyMuPDF (pip install pymupdf) or provide a Markdown "
            "version of the paper."
        )
        sys.exit(1)
    except Exception as e:
        print(f"ERROR:All extraction methods failed: {e}", file=sys.stderr)
        print(
            "ASK_USER:PDF extraction failed completely. "
            "Please provide a Markdown or text version of the paper."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
