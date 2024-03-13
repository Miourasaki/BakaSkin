from fastapi import APIRouter

router = APIRouter()

from . import texture, profile, join, secure

router.include_router(secure.router, prefix="")
router.include_router(join.router, prefix="")
router.include_router(profile.router, prefix="")
router.include_router(texture.router, prefix="")
