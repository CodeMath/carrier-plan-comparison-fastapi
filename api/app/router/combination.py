from fastapi import APIRouter, Query, HTTPException
from typing_extensions import Annotated
from typing import Union
from ..internal.calculater import (
    is_base_line,
    sum_of_payment,
)

from ..internal.planKT import (
    InternatCombination,
    CombinedDiscount,
    LineDiscount,
)

from ..fake_db.fake_db import fake_plan, fake_internet, fake_combination_rule


router = APIRouter(
    prefix="/combination",
    tags=["combination"],
    responses={404: {"description": "404 not found"}},
)


@router.get(
    "/kt",
    summary="combination of KT carrier plan",
    response_description="combination of KT carrier plan",
    response_model=CombinedDiscount,
    response_model_exclude_unset=True,
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
        raise HTTPException(status_code=404)

    # single combination
    if len(q) == 1:
        combination_rule = fake_combination_rule["single"]
        base_line["combination_rule"] = combination_rule
        base_line["contract_discount"] = 0.25
        base_line_model = LineDiscount(**base_line)

        single_combination = CombinedDiscount(
            base_line=base_line_model,
            internet=base_internet,
            sum_payment=sum_of_payment(base_line=base_line, ith=base_internet),
        )
        return single_combination
    else:
        # check 2 case
        for plan in stored_plan:
            pass

    # sum_price = 0
    # for splan in stored_plan:
    #     splan.price

    return stored_plan
