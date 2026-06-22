from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse, FileResponse
from services.YT import (
    yt_to_mp4,
    yt_to_m4a
)

router = APIRouter(tags=["YT"])

# YT -> Video
@router.post("/yt2mp4")
async def convert_yt_to_video(
    url: str = Form(..., description="youtube url.")
):
    try:
        file_name = await yt_to_mp4(
            url=url
        )
        return FileResponse(
            path=f"./fileProcessing/{file_name}.mp4",
            media_type="video/mp4",
            filename=f"{file_name}.mp4"
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "failed to fetch the video.",
                "reason": str(e)
            }
        )
    

# YT -> Audio
@router.post("/yt2m4a")
async def convert_yt_to_audio(
    url: str = Form(..., description="youtube url.")
):
    try:
        file_name = await yt_to_m4a(
            url=url
        )
        return FileResponse(
            path=f"./fileProcessing/{file_name}.m4a",
            media_type="audio/m4a",
            filename=f"{file_name}.m4a"
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "failed to fetch the audio.",
                "reason": str(e)
            }
        )