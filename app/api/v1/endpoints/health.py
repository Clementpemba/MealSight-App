from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def health_check():
    """Health check endpoint for API v1."""
    return {"status": "ok", "api_version": "v1"}
