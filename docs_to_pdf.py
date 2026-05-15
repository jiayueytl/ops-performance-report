import os
import win32com.client

def convert_to_pdf(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize both applications
    word = win32com.client.Dispatch("Word.Application")
    excel = win32com.client.Dispatch("Excel.Application")
    
    # Keep them hidden in the background
    word.Visible = False
    excel.Visible = False
    
    abs_input_dir = os.path.abspath(input_dir)
    abs_output_dir = os.path.abspath(output_dir)
    
    for filename in os.listdir(abs_input_dir):
        input_path = os.path.join(abs_input_dir, filename)
        base_name = os.path.splitext(filename)[0]
        output_path = os.path.join(abs_output_dir, f"{base_name}.pdf")

        try:
            # Handle Word Files
            if filename.lower().endswith((".docx", ".doc")):
                doc = word.Documents.Open(input_path)
                doc.SaveAs(output_path, FileFormat=17)
                doc.Close()
                print(f"Word Converted: {filename}")

            # Handle Excel Files
            elif filename.lower().endswith((".xlsx", ".xls", ".csv")):
                wb = excel.Workbooks.Open(input_path)
                # Type 0 = PDF
                wb.ExportAsFixedFormat(0, output_path)
                wb.Close(False) # False = Close without saving changes to original
                print(f"Excel Converted: {filename}")

        except Exception as e:
            print(f"Failed to convert {filename}: {e}")

    word.Quit()
    excel.Quit()

convert_to_pdf(
    input_dir=r'C:\Users\jiayue.tan\OneDrive - YTL\Workstation\dev\20260330-Amanah118_ThaiOCR_Ops\QUOTATION', 
    output_dir=r'C:\Users\jiayue.tan\OneDrive - YTL\Workstation\dev\20260330-Amanah118_ThaiOCR_Ops\QUOTATION'
)