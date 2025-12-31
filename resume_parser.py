import PyPDF2 as pdf
import docx

def extract_text_from_pdf(file):
    reader=pdf.PdfReader(file)
    text=""
    for page in reader.pages:
        text+=(page.extract_text() or "")+"\n"
    return text

def extract_text_from_docx(file):
    doc=docx.Document(file)
    text="\n".join([para.text for para in doc.paragraphs])
    return text

def parse_resume(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    else:
        raise ValueError("Unsupported file format. Please upload PDF or DOCX")

