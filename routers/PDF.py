import os
import tempfile
import shutil
import json
from fastapi import APIRouter, HTTPException, UploadFile, Form, File
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional
from services.PDF import (
    pdf_to_image, 
    pdf_compression, 
    pdf_delete_pages, 
    pdf_to_md, 
    pdf_to_text,
    text_to_pdf
)

router = APIRouter(tags=["PDF"])

# template endpoint
@router.post("/uploadpdf")
async def upload_pdf_file(
    file: UploadFile = File(..., description="upload a pdf file.")
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="only pdfs allowed"
        )
    
    return JSONResponse(
        status_code=200,
        content={
            "filename": file.filename, 
            "content-type": file.content_type, 
        }
    )


# PDF -> Every page to image
@router.post("/pdf2image")
async def convert_pdf_to_image(
    file: UploadFile = File(..., description="upload a pdf file.")
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="only pdfs allowed"
        )
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name
        file_name = file.filename[:-4]

    try:
        pdf_to_image(temp_path, file_name)
        return FileResponse(
            path=f"./fileProcessing/{file_name}.zip",
            media_type="application/x-zip-compressed",
            filename=f"{file_name}.zip"
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "failed to convert the pdf.",
                "reason": str(e)
            }
        )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


# PDF -> Start-End pages to image
@router.post("/pdf2image_range")
async def convert_pdf_to_image_range(
    file: UploadFile = File(..., description="upload a pdf file."),
    start: int = Form(gt=0, description="from _ page number."),
    end: Optional[int] = Form(None, description="till _ page number.")
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="only pdfs allowed"
        )
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name
        file_name = file.filename[:-4]

    try:
        pdf_to_image(
            pdf_path=temp_path, 
            pdf_name=file_name,
            start=start,
            end=end
        )
        return FileResponse(
            path=f"./fileProcessing/{file_name}.zip",
            media_type="application/x-zip-compressed",
            filename=f"{file_name}.zip"
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "failed to convert the pdf.",
                "reason": str(e)
            }
        )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


# PDF -> Specific pages to image
@router.post("/pdf2image_specific")
async def convert_pdf_to_image_specific(
    file: UploadFile = File(..., description="upload a pdf file."),
    pages: str = Form(..., description="list of page numbers, e.g., [1, 2, 3].")
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="only pdfs allowed"
        )

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name
        file_name = file.filename[:-4]

    clean_pages = pages.strip()

    try:
        pages_list = json.loads(clean_pages)
        if not isinstance(pages_list, list):
            pages_list = [pages_list]
    except (json.JSONDecodeError, TypeError):
        try:
            pages_list = [int(x.strip()) for x in clean_pages.split(",") if x.strip()]
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid format for pages. Use [1,2] or 1,2")

    try:
        pdf_to_image(
            pdf_path=temp_path, 
            pdf_name=file_name,
            pages=pages_list
        )
        return FileResponse(
            path=f"./fileProcessing/{file_name}.zip",
            media_type="application/x-zip-compressed",
            filename=f"{file_name}.zip"
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "failed to convert the pdf.",
                "reason": str(e)
            }
        )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


# PDF compressor
@router.post("/compress_pdf")
async def compress_pdf(
    file: UploadFile = File(..., description="upload a pdf file.")
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="only pdfs allowed"
        )
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name
        file_name = f"{file.filename[:-4]}_compressed"

    try:
        pdf_compression(
            pdf_path=temp_path,
            pdf_name=file_name
        )
        return FileResponse(
            path=f"./fileProcessing/{file_name}.pdf",
            media_type="application/pdf",
            filename=f"{file_name}.pdf"
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "failed to convert the pdf.",
                "reason": str(e)
            }
        )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


# PDF delete specific pages
@router.post("/pdf_delete_pages")
async def pdf_remove_pages(
    file: UploadFile = File(..., description="upload a pdf file."),
    pages: str = Form(..., description="list of page numbers, e.g., [1, 2, 3].")
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="only pdfs allowed"
        )
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name
        file_name = file.filename[:-4]

    clean_pages = pages.strip()

    try:
        pages_list = json.loads(clean_pages)
        if not isinstance(pages_list, list):
            pages_list = [pages_list]
    except (json.JSONDecodeError, TypeError):
        try:
            pages_list = [int(x.strip()) for x in clean_pages.split(",") if x.strip()]
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid format for pages. Use [1,2] or 1,2")

    try:
        pdf_delete_pages(
            pdf_path=temp_path,
            pdf_name=file_name,
            pages=pages_list
        )
        return FileResponse(
            path=f"./fileProcessing/{file_name}.pdf",
            media_type="application/pdf",
            filename=f"{file_name}.pdf"
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "failed to convert the pdf.",
                "reason": str(e)
            }
        )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


# PDF -> MD
@router.post("/pdf2md")
async def convert_pdf_to_md(
    file: UploadFile = File(..., description="upload a pdf file.")
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="only pdfs allowed"
        )
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name
        file_name = f"{file.filename[:-4]}"

    try:
        pdf_to_md(
            pdf_path=temp_path,
            pdf_name=file_name
        )
        return FileResponse(
            path=f"./fileProcessing/{file_name}.md",
            media_type="text/markdown",
            filename=f"{file_name}.md"
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "failed to convert the pdf.",
                "reason": str(e)
            }
        )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


# PDF -> Text
@router.post("/pdf2txt")
async def convert_pdf_to_txt(
    file: UploadFile = File(..., description="upload a pdf file.")
):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=415,
            detail="only pdfs allowed"
        )
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name
        file_name = f"{file.filename[:-4]}"

    try:
        pdf_to_text(
            pdf_path=temp_path,
            pdf_name=file_name
        )
        return FileResponse(
            path=f"./fileProcessing/{file_name}.txt",
            media_type="text/plain",
            filename=f"{file_name}.txt"
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "failed to convert the pdf.",
                "reason": str(e)
            }
        )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


# Text -> PDF
@router.post("/txt2pdf")
async def convert_txt_to_pdf(
    file: UploadFile = File(..., description="upload a txt file.")
):
    if file.content_type != "text/plain":
        raise HTTPException(
            status_code=415,
            detail="only txt files allowed"
        )
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_path = temp_file.name
        file_name = f"{file.filename[:-4]}"

    try:
        text_to_pdf(
            txt_path=temp_path,
            txt_name=file_name
        )
        return FileResponse(
            path=f"./fileProcessing/{file_name}.pdf",
            media_type="application/pdf",
            filename=f"{file_name}.pdf"
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "failed to convert text files.",
                "reason": str(e)
            }
        )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)