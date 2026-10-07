"""PDF merging logic, kept separate from the user interface."""

from pathlib import Path

from pypdf import PdfReader, PdfWriter


def count_pages(path):
    """Return the number of pages in a PDF."""
    return len(PdfReader(path).pages)


def merge_pdfs(input_paths, output_path):
    """Combine any number of PDFs, in the given order, into one file."""
    if not input_paths:
        raise ValueError("No PDF files to merge.")

    writer = PdfWriter()
    for path in input_paths:
        writer.append(Path(path))

    with open(output_path, "wb") as f:
        writer.write(f)
    writer.close()
