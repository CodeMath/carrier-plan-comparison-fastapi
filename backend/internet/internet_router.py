from fastapi import APIRouter, Query, HTTPException, Depends
from typing_extensions import Annotated
from typing import Union

from dependency import get_db  # SessionLocal()

from internet import internet_schemas
from internet import internet_crud
from db.models import model_internet

from sqlalchemy.orm import Session

from starlette import status


router = APIRouter(
    prefix="/api/internet",
    tags=["internet"],
    responses={404: {"description": "404 not found"}},
)


@router.post(
    "/create/internet",
)
async def create_internet(
    internet: internet_schemas.CreateInternet_Schema, db: Session = Depends(get_db)
):
    """Create Internet Plan"""
    exist_internet_plan = internet_crud.get_existing_internet(db, internet=internet)

    if exist_internet_plan:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Already registered"
        )
    return internet_crud.create_internet(db=db, internet=internet)


@router.get(
    "/get/internet",
    summary="Get KT internet plan by title",
    response_description="Get KT internet plan by title",
    response_model=list[internet_schemas.Internet],
)
async def internet_item_by_title(title_list: list[str], db: Session = Depends(get_db)):
    """
    Get KT carrier plan by titles
    - **title_list**: ["슬림"]
    """
    result = []
    for title in title_list:
        existing_internet = internet_crud.get_internet_by_title(db=db, title=title)
        if existing_internet:
            result.append(existing_internet)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="400 Error - internnet title: {}".format(title),
            )
    return result


@router.get(
    "/all/internet",
    summary="All KT Internet plan",
    response_model=internet_schemas.InternetList,
)
async def internet_items_list(
    db: Session = Depends(get_db),
    page: int = 0,
    size: int = 10,
    price: int = 0,
    title: str = "",
):
    total, _internet_list = internet_crud.get_internet_list(
        db, skip=page * size, limit=size, price=price, title=title
    )
    return {"total": total, "internet_list": _internet_list}


@router.update(
    "/update/internet",
    summary="update internet",
    status_cdoe=status.HTTP_204_NO_CONTENT,
)
async def internet_update(
    db: Session, _internet_update=internet_schemas.UpdateInternet_Schema
):
    db_internet = internet_crud.get_internet_by_id(
        db=db, internet_id=_internet_update.internet_id
    )
    if not db_internet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="400 Error - not found"
        )

    internet_crud.update_internet(
        db=db, db_internet=db_internet, mobile_update=_internet_update
    )


@router.delete("/delete/internet", status_code=status.HTTP_204_NO_CONTENT)
async def internet_delete(
    db: Session, _internet_delete: internet_schemas.DeleteInternet_Schema
):
    db_internet = internet_crud.get_internet_by_id(
        db=db, internet_id=_internet_delete.internet_id
    )
    if not db_internet:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="400 Error - not found"
        )

    internet_crud.delete_internet(db=db, db_internet=db_internet)
