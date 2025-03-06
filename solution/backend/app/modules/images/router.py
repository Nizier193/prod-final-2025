# HTTP

from fastapi import APIRouter, Depends, File, Query, Request, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse

from redis import Redis
from sqlalchemy.orm import Session
from uuid import UUID

from common.dependencies import get_campaign_service_repo
from core.database import get_db
from core.cache import get_cache
from core.boto import get_boto
from .repository import BotoRepository


router = APIRouter()

@router.post("/{campaignId}")
def upload_image(
    campaignId: UUID,
    image: UploadFile = File(...),
    boto = Depends(get_boto),
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    campaign_repo = get_campaign_service_repo(db)
    boto_repo = BotoRepository(boto)

    campaign = campaign_repo.get_campaign_by_id(campaignId)
    if not campaign:
        return JSONResponse(content={"error": "no campaign with that id"}, status_code=404)

    status = boto_repo.upload_image(
        campaignId=campaignId,
        image_name=image.filename if image.filename else f"{campaignId}.png",
        image=image.file
    )

    if not status.status:
        return JSONResponse(content={"error": "error while trying to upload image"}, status_code=400)

    
    return JSONResponse(
        content=jsonable_encoder(status.model_dump(exclude_none=True)),
        status_code=201
    )


@router.get("/{campaignId}")
def get_images(
    request: Request,
    campaignId: UUID,
    limit: int = Query(default=10e3, ge=1),
    offset: int = Query(default=0, ge=0),
    boto = Depends(get_boto),
    db: Session = Depends(get_db),
    cache: Redis = Depends(get_cache)
):
    base_url = str(request.base_url)
    campaign_repo = get_campaign_service_repo(db)
    boto_repo = BotoRepository(boto)

    campaign = campaign_repo.get_campaign_by_id(campaignId)
    if not campaign:
        return JSONResponse(content={"error": "no campaign with that id"}, status_code=404)
    
    status = boto_repo.get_images_by_campaign_id(
        campaignId=campaignId,
        limit=limit,
        offset=offset
    )
    
    return JSONResponse(
        content=jsonable_encoder(status),
        status_code=200
    )
    


@router.get("/")
async def get_image_by_key(
    key: str = Query(...),
    boto = Depends(get_boto),
):
    boto_repo = BotoRepository(boto)
    result = boto_repo.get_image_by_key(key=key)
    
    if not result:
        return JSONResponse(status_code=404, content={"error": "Image not found"})
    
    body, content_type = result
    
    headers = {}
    headers["Content-Disposition"] = "inline"
    headers["Content-Disposition"] = f'attachment; filename="{key.split("/")[-1]}"'
    
    return StreamingResponse(
        body,
        media_type=content_type or 'application/octet-stream',
        headers=headers
    )
