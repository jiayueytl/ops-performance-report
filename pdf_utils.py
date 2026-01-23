import os
import pdfkit
import io
from datetime import datetime

def get_wkhtml_config():
    """Locates the binary without requiring admin elevation."""
    path_wkhtmltopdf = os.path.join(os.getcwd(), "wkhtmltopdf/bin", "wkhtmltopdf.exe")
    if not os.path.exists(path_wkhtmltopdf):
        return None
    return pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

def generate_pdf_bytes(html_content):
    config = get_wkhtml_config()
    if not config:
        raise FileNotFoundError("wkhtmltopdf binary not found. Please check paths.")

    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'no-outline': None,
        'quiet': ''
    }
    return pdfkit.from_string(html_content, False, options=options, configuration=config)