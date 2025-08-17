from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends as FDepends
from ab_core.database.session_context import db_session_async
from ab_core.dependency import Depends
from ab_core.user.model import User
from ab_core.user.service import UserService
from sqlalchemy.ext.asyncio.session import AsyncSession

router = APIRouter(
    prefix="/user",
    tags=["Template"],
)


@router.get(
    "/{user_id}",
    response_model=User,
)
async def get_user_by_id(
    user_id: str,
    db_session: Annotated[
        AsyncSession,
        FDepends(db_session_async),
    ],
    user_service: Annotated[
        UserService,
        Depends(UserService, persist=True),
    ],
):
    return await user_service.get_user_by_id(
        user_id=user_id,
        db_session=db_session,
    )
