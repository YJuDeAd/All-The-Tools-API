import os
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from routers import PDF

os.makedirs("fileProcessing", exist_ok=True)

app = FastAPI(title="All The Tools - API")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "status": "error",
            "message": "Invalid request payload.",
            "details": exc.errors(),
        },
    )

app.include_router(PDF.router, prefix="/api/v1")