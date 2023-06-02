from fastapi import Depends, APIRouter, Query, HTTPException
from typing_extensions import Annotated
from typing import Union
from pydantic import Required

from ..internal.planKT import PlanKT, fake_plan, InternatCombination, fake_internet
from ..dependency import carrier_type


router = APIRouter(
    prefix="/plan", tags=["plan"], responses={404: {"description": "404 not found"}}
)


@router.get(
    "/kt",
    response_model=list[PlanKT],
    response_model_exclude_unset=True,
    summary="Get list KT carrier plan",
    response_description="Get list KT carrier plan",
)
async def get_items(
    price: Annotated[int, Query(ge=0)] = 0,
    tp: Annotated[str, Query(examples=carrier_type)] = "all",
):
    """
    Get list of KT carrier plan for "가족 프리미엄 결합", "총액결합" and "싱글결합"
    - price: price
    - tp: 5g / LTE / all
    """
    if price:
        ge_plan = []
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

    return [plan for plan in fake_plan.values()]


def is_base_line(plan: list[PlanKT]):
    return min(plan, key=lambda x: x["price"])


@router.get(
    "/kt/combination",
    summary="combination of KT carrier plan",
    response_description="combination of KT carrier plan",
)
async def select_carrier(
    q: Annotated[
        Union[list[str], None],
        Query(
            min_lenght=1,
            examples=fake_plan,
        ),
    ],
    ith: Annotated[str, Query(examples=fake_internet)],
):
    """
    - **q**: each KT plan name
    """
    try:
        stored_plan = [fake_plan[name] for name in q]
        base_line = is_base_line(stored_plan)
    except KeyError:
        raise HTTPException(status_code=404)

    try:
        internet = fake_internet[ith]
        base_internet = InternatCombination(**internet)
    except KeyError:
        internet = {}
        base_internet = InternatCombination(internet=ith)

    # single combination
    if len(q) == 1:
        stored_plan[0].update(
            {
                "title": "싱글 결합",
                "contract_discount_25%": base_line["price"] * 0.25,
                "single_contract_discount_25%": base_line["price"] * 0.25,
                "discount_sum": base_line["price"] * 0.5,
                "internet": base_internet,
                "payment": base_line["price"] * 0.5 + base_internet.price,
            }
        )
    else:
        # check 2 case
        for plan in stored_plan:
            pass

    # sum_price = 0
    # for splan in stored_plan:
    #     splan.price

    return stored_plan
