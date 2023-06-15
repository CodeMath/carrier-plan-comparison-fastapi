from fastapi import APIRouter, Query, HTTPException, Depends
from typing_extensions import Annotated
from typing import Union
from db.models.modle_kt_schemas import PlanKT, InternatCombination, Internets
from fake_db.fake_db import fake_plan, fake_internet


router = APIRouter(
    prefix="/plan", tags=["plan"], responses={404: {"description": "404 not found"}}
)


from sqlalchemy.orm import Session
from .crud import *
from db.models.mobile_plan import *
from db.session import *


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/mobile", response_model=PlanKTinDB)
def create_plan(plan: PlanKTinDB, db: Session = Depends(get_db)):
    """
    Error 나옴... 수정 필요
    """
    db_plan_ko_title = get_plan_by_ko_name(db=db, title=plan.title)
    print(db_plan_ko_title)
    if db_plan_ko_title:
        raise HTTPException(status_code=400, detail="Already registered")
    return create_plan(db=db, plan=plan)


@router.get(
    "/get/mobile",
    summary="Get KT carrier plan by title",
    response_description="Get KT carrier plan by title",
)
async def get_mobile_item(
    titles: Annotated[
        Union[list[str], None],
        Query(
            examples=fake_plan,
        ),
    ],
    db: Session = Depends(get_db),
):
    """
    Get KT carrier plan by titles
    - **titles**: ["초이스 프리미엄", "베이직"]
    """
    result = []
    for title in titles:
        # find_plan = [plan for plan in fake_plan.values() if plan["title"] == title]
        find_plan = get_plan_by_ko_name(db, title=title)
        if find_plan:
            result.append(find_plan[0])
        else:
            raise HTTPException(status_code=404)
    return result


@router.get(
    "/list/mobile",
    response_model=list[PlanKT],
    response_model_exclude_unset=True,
    summary="Get list KT carrier plan",
    response_description="Get list KT carrier plan",
)
async def get_list_mobile_items(
    price: Annotated[int, Query(ge=0)] = 0,
    tp: Annotated[str, Query(example="all")] = "all",
):
    """
    Get list of KT carrier plan for "가족 프리미엄 결합", "총액결합" and "싱글결합"
    - **price**: default:0
    - **tp**: 5g / LTE / all
    """
    ge_plan = []
    if price:
        for plan in fake_plan.values():
            if plan["price"] >= price:
                if tp == "all":
                    ge_plan.append(plan)
                elif tp.upper() == "5G" and plan["carrier"] == "5G":
                    ge_plan.append(plan)
                elif tp.upper() == "LTE" and plan["carrier"] == "LTE":
                    ge_plan.append(plan)
        if ge_plan:
            return ge_plan
        else:
            raise HTTPException(status_code=404)
    if tp:
        for plan in fake_plan.values():
            if plan["carrier"] == tp.upper():
                ge_plan.append(plan)

        if ge_plan:
            return ge_plan
        else:
            raise HTTPException(status_code=404)

    return [plan for plan in fake_plan.values()]


@router.get(
    "/get/internet",
    summary="Get KT internet plan by title",
    response_description="Get KT internet plan by title",
    response_model=Internets,
    response_model_exclude_unset=True,
)
async def get_internet_item(
    title: Annotated[
        Union[str, None],
        Query(
            examples=fake_internet,
        ),
    ]
):
    """
    Get KT carrier plan by titles
    - **title**: ["슬림"]
    """
    find_plan = [plan for plan in fake_internet.values() if plan["internet"] == title]
    if find_plan:
        eng_internet = [
            key for key, plan in fake_internet.items() if find_plan[0] == plan
        ]
        find_plan[0]["eng_internet"] = eng_internet[0]
        return find_plan[0]
    else:
        raise HTTPException(status_code=404)


@router.get(
    "/list/internet",
    response_model=list[InternatCombination],
    response_model_exclude_unset=True,
    summary="Get list KT internet plan",
    response_description="Get list KT internet plan",
)
async def get_list_internet_items(
    price: Annotated[int, Query(ge=0)] = 0,
    wifi: Annotated[int, Query(ge=-1, le=2)] = -1,
):
    """
    Get list of KT internet plan
    - **price**: default:0
    - **wifi**: how many giga wifi 0,1,2 / -1 : all
    """
    ge_plan = []
    if price > 0:
        for plan in fake_internet.values():
            if plan["price"] >= price:
                if wifi == -1:
                    ge_plan.append(plan)
                elif wifi == plan["wifi"]:
                    ge_plan.append(plan)

        if ge_plan:
            return ge_plan
        else:
            raise HTTPException(status_code=404)
    if wifi == -1:
        return [plan for plan in fake_internet.values()]
    else:
        for plan in fake_internet.values():
            if wifi == plan["wifi"]:
                ge_plan.append(plan)

        if ge_plan:
            return ge_plan
        else:
            raise HTTPException(status_code=404)
