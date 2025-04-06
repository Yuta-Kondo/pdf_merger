import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def add_filename_watermark(input_pdf_path, output_pdf_path, filename):
    """Add filename watermark to each page of a PDF"""
    # Create a watermark PDF with the filename
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica", 10)
    can.setFillColorRGB(0.5, 0.5, 0.5)  # Gray color
    # Position text at bottom right (adjust as needed)
    can.drawRightString(letter[0] - 20, 20, f"Source: {filename}")
    can.save()
    
    # Move to the beginning of the BytesIO buffer
    packet.seek(0)
    watermark_pdf = PdfReader(packet)
    watermark_page = watermark_pdf.pages[0]
    
    # Read the input PDF
    pdf_reader = PdfReader(input_pdf_path)
    pdf_writer = PdfWriter()
    
    # Apply watermark to each page
    for page in pdf_reader.pages:
        page.merge_page(watermark_page)
        pdf_writer.add_page(page)
    
    # Write the watermarked PDF
    with open(output_pdf_path, "wb") as output_pdf:
        pdf_writer.write(output_pdf)

def merge_pdfs_with_filenames(pdf_files, output_filename):
    """Merge multiple PDFs with filename watermarks"""
    pdf_writer = PdfWriter()
    
    for pdf_file in pdf_files:
        # Create a temporary watermarked version
        temp_filename = f"temp_{os.path.basename(pdf_file)}"
        add_filename_watermark(pdf_file, temp_filename, os.path.basename(pdf_file))
        
        # Add watermarked pages to the merger
        pdf_reader = PdfReader(temp_filename)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
        
        # Clean up temporary file
        os.remove(temp_filename)
    
    # Write the merged output
    with open(output_filename, "wb") as out:
        pdf_writer.write(out)
    
    print(f"Merged PDF saved as {output_filename}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python pdf_merger.py output.pdf input1.pdf input2.pdf ...")
        sys.exit(1)
    
    output_file = sys.argv[1]
    input_files = sys.argv[2:]
    
    # Verify files exist
    for f in input_files:
        if not os.path.isfile(f):
            print(f"Error: File not found - {f}")
            sys.exit(1)
    
    merge_pdfs_with_filenames(input_files, output_file)
    