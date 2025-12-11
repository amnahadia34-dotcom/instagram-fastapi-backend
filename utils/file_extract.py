from PyPDF2 import PdfReader
import docx
import tempfile

async def extract_text_from_file(file):
    ext = file.filename.split(".")[-1].lower()
    contents = await file.read()
    text = ""
    if ext == "pdf":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(contents)
            tmp.close()
            reader = PdfReader(tmp.name)
            for page in reader.pages:
                text += page.extract_text() or ""
    elif ext in ["docx", "doc"]:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
            tmp.write(contents)
            tmp.close()
            doc = docx.Document(tmp.name)
            for para in doc.paragraphs:
                text += para.text + "\n"
    else:
        raise Exception("Unsupported file type.")
    return text
