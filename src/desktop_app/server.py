from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, ConfigDict, HttpUrl

from doubao_parser.image import doubao_image_parse
from doubao_parser.video import doubao_video_parse
from src.desktop_app.runtime import ui_dir


class ImageRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"url": "https://www.doubao.com/thread/example", "return_raw": False}}
    )

    url: HttpUrl
    return_raw: bool = False


class ImageResponse(BaseModel):
    success: bool
    image_count: int
    images: list[dict]


class VideoRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "url": "https://www.doubao.com/video-sharing?share_id=xxx&video_id=xxx",
                "return_raw": False,
            }
        }
    )

    url: HttpUrl
    return_raw: bool = False


class VideoResponse(BaseModel):
    success: bool
    video: dict


def _frontend_file() -> Path:
    return ui_dir() / "index.html"


def create_app() -> FastAPI:
    app = FastAPI(
        title="doubao-no-watermarking API",
        description="Extract images and videos from Doubao share links.",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", include_in_schema=False)
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/", include_in_schema=False)
    async def root():
        frontend = _frontend_file()
        if frontend.exists():
            return FileResponse(frontend)
        return {"message": "doubao-no-watermarking API", "docs": "/docs", "version": "1.0.0"}

    @app.post("/parse", summary="Parse image share links")
    async def parse_image(request: ImageRequest):
        return await _parse_image(str(request.url), request.return_raw)

    @app.get("/parse", summary="Parse image share links (GET)")
    async def parse_image_get(url: str, return_raw: bool = False):
        return await _parse_image(url, return_raw)

    @app.post("/parse-video", summary="Parse video share links")
    async def parse_video(request: VideoRequest):
        return await _parse_video(str(request.url), request.return_raw)

    @app.get("/parse-video", summary="Parse video share links (GET)")
    async def parse_video_get(url: str, return_raw: bool = False):
        return await _parse_video(url, return_raw)

    return app


async def _parse_image(url: str, return_raw: bool):
    try:
        result = await doubao_image_parse(url, return_raw=return_raw)
        if return_raw:
            return {"success": True, "data": result}
        return ImageResponse(success=True, image_count=len(result), images=result)
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        print(f"Image parsing exception: {exc}")
        raise HTTPException(status_code=500, detail="Image parsing failed. Please verify the shared link.") from exc


async def _parse_video(url: str, return_raw: bool):
    try:
        result = await doubao_video_parse(url, return_raw=return_raw)
        if return_raw:
            return {"success": True, "data": result}
        return VideoResponse(success=True, video=result)
    except (ValueError, KeyError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        print(f"Video parsing exception: {exc}")
        raise HTTPException(status_code=500, detail="Video parsing failed. Please verify the shared link.") from exc


app = create_app()
