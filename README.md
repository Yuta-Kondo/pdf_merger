# PDF Merger with Filename Watermarks

A Python utility that merges multiple PDF files into a single document while adding a watermark with the source filename to each page.

## Features

- Merge multiple PDF files into a single document
- Add a watermark with the source filename to each page
- Preserves all PDF content and formatting

## Requirements

- Python 3.6+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python pdf_merger.py output.pdf input1.pdf input2.pdf [input3.pdf ...]
```

### Arguments

- `output.pdf`: The filename for the merged output PDF
- `input1.pdf`, `input2.pdf`, etc.: The PDF files to merge (at least one required)

## Example

```bash
python pdf_merger.py merged_document.pdf chapter1.pdf chapter2.pdf appendix.pdf
```

This will create a file called `merged_document.pdf` containing all pages from the input PDFs, with each page watermarked with its source filename.

## How It Works

The script performs the following steps:

1. For each input PDF, it creates a temporary version with the filename watermarked on each page
2. It then merges all these temporary PDFs into the final output file
3. The temporary files are automatically cleaned up after processing

## License

MIT
