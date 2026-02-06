import os
from pdf2docx import Converter
from docx2pdf import convert

def convert_doc(input_path, target_format, state_ref):
    try:
        if not os.path.exists(input_path):
            return "Error: File tidak ditemukan."

        state_ref["status_text"] = f"Mengonversi ke {target_format}..."
        state_ref["progress"] = 0.3 # Mulai jalan
        
        directory = os.path.dirname(input_path)
        filename = os.path.basename(input_path)
        name_no_ext = os.path.splitext(filename)[0]
        
        if target_format == "DOCX" and input_path.lower().endswith(".pdf"):
            output_path = os.path.join(directory, f"{name_no_ext}.docx")
            cv = Converter(input_path)
            cv.convert(output_path, start=0, end=None)
            cv.close()
            
            state_ref["progress"] = 1.0
            state_ref["is_processing"] = False
            return f"Sukses: {output_path}"

        elif target_format == "PDF" and input_path.lower().endswith(".docx"):
            output_path = os.path.join(directory, f"{name_no_ext}.pdf")
            convert(input_path, output_path)
            
            state_ref["progress"] = 1.0
            state_ref["is_processing"] = False
            return f"Sukses: {output_path}"

        state_ref["is_processing"] = False
        return "Error: Format tidak sesuai."

    except Exception as e:
        state_ref["is_processing"] = False
        return f"Error System: {str(e)}"