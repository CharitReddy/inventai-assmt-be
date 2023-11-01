from fastapi import APIRouter, HTTPException

router = APIRouter()

# Wild card path - Return a 404 Not Found on any non existing API path.
@router.get("/{path:path}")
async def not_found(path: str):
    raise HTTPException(status_code=404, detail="Path does not exist")