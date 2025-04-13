import os
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
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
    
    return f"Merged PDF saved as {output_filename}"

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("600x500")
        self.root.minsize(500, 400)
        
        self.pdf_files = []
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="PDF Merger", font=("Helvetica", 16))
        title_label.pack(pady=10)
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="Select PDF Files", padding="10")
        file_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Buttons frame
        btn_frame = ttk.Frame(file_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        # Add files button
        add_btn = ttk.Button(btn_frame, text="Add PDF Files", command=self.add_files)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Remove selected button
        remove_btn = ttk.Button(btn_frame, text="Remove Selected", command=self.remove_selected)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear all button
        clear_btn = ttk.Button(btn_frame, text="Clear All", command=self.clear_files)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Files listbox with scrollbar
        list_frame = ttk.Frame(file_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.files_listbox = tk.Listbox(list_frame, selectmode=tk.EXTENDED)
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_listbox.config(yscrollcommand=scrollbar.set)
        
        # Output file section
        output_frame = ttk.LabelFrame(main_frame, text="Output File", padding="10")
        output_frame.pack(fill=tk.X, padx=5, pady=5)
        
        output_inner_frame = ttk.Frame(output_frame)
        output_inner_frame.pack(fill=tk.X, expand=True)
        
        self.output_var = tk.StringVar(value="merged_output.pdf")
        output_entry = ttk.Entry(output_inner_frame, textvariable=self.output_var, width=40)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        browse_btn = ttk.Button(output_inner_frame, text="Browse", command=self.browse_output)
        browse_btn.pack(side=tk.RIGHT, padx=5)
        
        # Merge button
        merge_btn = ttk.Button(main_frame, text="Merge PDFs", command=self.merge_pdfs)
        merge_btn.pack(pady=10)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if files:
            for file in files:
                if file not in self.pdf_files:
                    self.pdf_files.append(file)
                    self.files_listbox.insert(tk.END, os.path.basename(file))
            
            self.status_var.set(f"{len(self.pdf_files)} files selected")
    
    def remove_selected(self):
        selected_indices = self.files_listbox.curselection()
        
        if not selected_indices:
            return
        
        # Remove in reverse order to avoid index shifting
        for i in sorted(selected_indices, reverse=True):
            del self.pdf_files[i]
            self.files_listbox.delete(i)
        
        self.status_var.set(f"{len(self.pdf_files)} files selected")
    
    def clear_files(self):
        self.pdf_files.clear()
        self.files_listbox.delete(0, tk.END)
        self.status_var.set("Ready")
    
    def browse_output(self):
        output_file = filedialog.asksaveasfilename(
            title="Save Merged PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )
        
        if output_file:
            self.output_var.set(output_file)
    
    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showwarning("No Files", "Please add PDF files to merge.")
            return
        
        output_file = self.output_var.get()
        
        if not output_file:
            messagebox.showwarning("No Output File", "Please specify an output file name.")
            return
        
        try:
            # Show progress
            self.status_var.set("Merging PDFs...")
            self.root.update_idletasks()
            
            # Perform the merge
            result = merge_pdfs_with_filenames(self.pdf_files, output_file)
            
            # Show success message
            messagebox.showinfo("Success", result)
            self.status_var.set(result)
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error occurred during merge")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
