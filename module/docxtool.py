import os
from pdf2docx import Converter
from docx2pdf import convert

def convert_doc(input_path, target_format):
    try:
        if not os.path.exists(input_path):
            return "Error: File tidak ditemukan."

        directory = os.path.dirname(input_path)
        filename = os.path.basename(input_path)
        name_no_ext = os.path.splitext(filename)[0]
        
        # LOGIC PDF TO DOCX
        if target_format == "DOCX" and input_path.lower().endswith(".pdf"):
            output_path = os.path.join(directory, f"{name_no_ext}.docx")
            cv = Converter(input_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()
            return f"Sukses: {output_path}"

        # LOGIC DOCX TO PDF
        elif target_format == "PDF" and input_path.lower().endswith(".docx"):
            output_path = os.path.join(directory, f"{name_no_ext}.pdf")
            convert(input_path, output_path)
            return f"Sukses: {output_path}"

        else:
            return "Error: Format file input tidak sesuai dengan target konversi."

    except Exception as e:
        return f"Error System: {str(e)}"