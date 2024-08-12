import fitz  # type: ignore # PyMuPDF
from PIL import Image
import io

def get_pdf_pages_as_text(book):
    try:
        pdf_document = fitz.open(book.pdf_file.path)
        pages_text = []
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text("text")
            pages_text.append(page_text)
        return pages_text
    except book.DoesNotExist:
        print("couldn't Extract PDF text")


def get_pdf_pages_as_images(book):
    pdf_document = fitz.open(book.pdf_file.path)
    pages = []
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes()))
        pages.append(img)
    return pages