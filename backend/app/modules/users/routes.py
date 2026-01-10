from fastapi import APIRouter, HTTPException

from app.core.config import get_settings

from .repository import get_user, init_db, upsert_user
from .schemas import UserOut, UserUpsert

router = APIRouter(prefix="/api/users", tags=["users"])


def _database_url() -> str:
    return get_settings().database_url


def init_module() -> None:
    init_db(_database_url())


@router.get("/me", response_model=UserOut)
def get_user_route() -> UserOut:
    user = get_user(_database_url())
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/me", response_model=UserOut)
def upsert_user_route(payload: UserUpsert) -> UserOut:
    return upsert_user(_database_url(), payload)
