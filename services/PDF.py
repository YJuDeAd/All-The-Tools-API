import os
import tempfile
import zipfile
import img2pdf
import fitz
import pymupdf4llm
import pymupdf
import pathlib
from pdf2image import convert_from_path


def pdf_to_image(
        pdf_path,
        pdf_name: str,
        start: int = 1,
        end: int = None,
        pages: list = None
):
    images = convert_from_path(pdf_path)
    
    if not pages:
        if not end:
            end = len(images)
        pages = [i+1 for i in range(start-1, end)]

    with zipfile.ZipFile(f"./fileProcessing/{pdf_name}.zip", "w") as zipf:
        for i in pages:
            file_name = f"./fileProcessing/{i}.png"
            images[i-1].save(file_name, "PNG")
            zipf.write(file_name, arcname=f"{i}.png")
            os.remove(file_name)


def pdf_compression(
        pdf_path,
        pdf_name: str
):
    pdf = fitz.open(pdf_path)

    pdf.scrub(
        metadata=True,
        attached_files=True,
        clean_pages=False
    )

    pdf.save(
        f"./fileProcessing/{pdf_name}.pdf",
        garbage=4,
        deflate=True,
        use_objstms=True
    )

    pdf.close()


def image_to_pdf(
        pdf_name: str,
        image_paths: list
):
    with open(f"./fileProcessing/{pdf_name}.pdf", "wb") as f:
        f.write(img2pdf.convert(image_paths))


def pdf_delete_pages(
        pdf_path,
        pdf_name: str,
        pages: list
):
    images = convert_from_path(pdf_path)
    image_paths = []

    for i, img in enumerate(images):
        if i + 1 not in pages:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                temp_path = temp_file.name
                
            img.save(temp_path, "PNG")
            image_paths.append(temp_path)

    image_to_pdf(pdf_name, image_paths)

    for temp_image in image_paths:
        if os.path.exists(temp_image):
            os.remove(temp_image)


def pdf_to_md(
        pdf_path,
        pdf_name: str
):
    md_text = pymupdf4llm.to_markdown(pdf_path)
    pathlib.Path(f"./fileProcessing/{pdf_name}.md").write_bytes(md_text.encode())


def pdf_to_text(
        pdf_path,
        pdf_name: str
):
    with pymupdf.open(pdf_path) as doc:
        text = chr(12).join([page.get_text() for page in doc])
    pathlib.Path(f"./fileProcessing/{pdf_name}.txt").write_bytes(text.encode())


def text_to_pdf(
        txt_path,
        txt_name: str
):
    doc = pymupdf.open(txt_path, filetype="txt")
    pdf_bytes = doc.convert_to_pdf()
    with open(f"./fileProcessing/{txt_name}.pdf", "wb") as f:
        f.write(pdf_bytes)