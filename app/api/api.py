from fastapi import APIRouter
from .endpoints import hello,generateemails,wildcard

router = APIRouter()
router.include_router(hello.router, prefix="/hello", tags=["Connection Test"])
router.include_router(generateemails.router, prefix="/generate_emails", tags=["Generate emails using Open AI APIs"])
# router.include_router(wildcard.router, tags=["Non Existing Paths"])

