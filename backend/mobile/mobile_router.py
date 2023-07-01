from fastapi import APIRouter, Query, HTTPException, Depends
from typing_extensions import Annotated
from typing import Union
from dependency import get_db  # SessionLocal()
from fastapi.encoders import jsonable_encoder
from mobile import mobile_schemas
from mobile import mobile_crud
from db.models import model_mobile

from sqlalchemy.orm import Session

from starlette import status


router = APIRouter(
    prefix="/api/mobile",
    tags=["mobile"],
    responses={404: {"description": "404 not found"}},
)


@router.post("/create/mobile", status_code=status.HTTP_204_NO_CONTENT)
async def mobile_create(
    plan: mobile_schemas.CreateMobile_Schema, db: Session = Depends(get_db)
):
    """Create Mobile Plan"""

    exist_mobile_plan = mobile_crud.get_existing_mobile(db, mobile=plan)

    if exist_mobile_plan:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Already registered"
        )
    return mobile_crud.create_mobile(db=db, mobile=plan)


@router.get(
    "/all/mobile",
    summary="All KT carrier plan",
    response_model=mobile_schemas.MobileList,
)
async def mobile_items_list(
    db: Session = Depends(get_db),
    page: int = 0,
    size: int = 10,
    price: int = 0,
    carrier: str = "",
):
    total, _mobile_list = mobile_crud.get_mobile_list(
        db, skip=page * size, limit=size, price=price, carrier=carrier
    )
    return {"total": total, "mobile_list": _mobile_list}


@router.post(
    "/get/mobile/plan/list",
    summary="Get list of KT carrier plan by title",
    response_description="Get list of Get KT carrier plan by title",
    response_model=mobile_schemas.MobileList,
)
async def mobile_item_by_title(
    title_list: list[str],
    db: Session = Depends(get_db),
):
    mobile_lisst = []
    count = 0
    for plan in title_list:
        find_plan = mobile_crud.get_mobile_by_title(db, mobile_plan=plan)
        if find_plan:
            print(find_plan)
            mobile_lisst.append(mobile_schemas.Mobile(find_plan))
            count += 1
    result = {"total": count, "mobiel_list": mobile_lisst}
    return mobile_schemas.MobileList(**result)


# 왜 modelMetaclass 에러가 날까?
# @router.put(
#     "/update/mobile", summary="update mobile", status_code=status.HTTP_204_NO_CONTENT
# )
# async def mobile_update(
#     _mobile_update=mobile_schemas.UpdateMobile_Schema, db: Session = Depends(get_db)
# ):
#     db_mobile = mobile_crud.get_mobile_by_id(db=db, mobile_id=_mobile_update.mobile_id)
#     if not db_mobile:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="400 Error - not found"
#         )

#     mobile_crud.update_mobile(db=db, db_mobile=db_mobile, mobile_update=_mobile_update)


@router.post("/delete/mobile", status_code=status.HTTP_204_NO_CONTENT)
async def mobile_delete(
    _mobile_delete: mobile_schemas.DeleteMobile_Schema, db: Session = Depends(get_db)
):
    db_mobile = mobile_crud.get_mobile_by_id(db=db, mobile_id=_mobile_delete.mobile_id)
    if not db_mobile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="400 Error - not found"
        )

    mobile_crud.delete_mobile(db=db, db_mobile=db_mobile)
