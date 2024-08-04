import fitz  # type: ignore # PyMuPDF
from PIL import Image
import io

def get_pdf_pages(book):
    pdf_document = fitz.open(book.pdf_file.path)
    pages = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pages.append(page.get_text("text"))
    return pages



def get_pdf_pages_as_images(book):
    pdf_document = fitz.open(book.pdf_file.path)
    pages = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))
        pages.append(img)
    return pages