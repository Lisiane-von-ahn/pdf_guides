from pdf2docx import Converter
from io import BytesIO
import base64

def generateTempFile(pdf_content, isPdf):
    pdf_buffer = BytesIO(pdf_content)
    pdf_buffer.seek(0)
    
    if(isPdf):
        with open('temp.pdf', 'wb') as temp_pdf:
            temp_pdf.write(pdf_buffer.getbuffer())
    else:
        with open('temp.docx', 'wb') as temp_docx:
            temp_docx.write(pdf_buffer.getbuffer())
        
def convert_pdf_to_docx(pdf_content):
    docx_buffer = BytesIO()
    
    cv = Converter('temp.pdf')
    cv.convert(docx_buffer, start=0, end=None)
    cv.close()
    
    docx_buffer.seek(0)
    return docx_buffer

def generate_download_link_doc(file_name, docx_buffer):
    base64_doc = base64.b64encode(docx_buffer.getvalue()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{base64_doc}" download="{file_name}">Télécharger le fichier DOCX</a>'
    return href

