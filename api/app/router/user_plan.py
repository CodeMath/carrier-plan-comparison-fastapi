from fastapi import APIRouter, Query, HTTPException
from typing_extensions import Annotated
from typing import Union

from ..internal.planKT import (
    PlanKT,
    fake_plan,
    InternatCombination,
    fake_internet,
    CombinedDiscount,
    LineDiscount,
    fake_combination_rule,
)
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


def calculate_contract_contract(line_model: LineDiscount):
    line = LineDiscount(**line_model)
    sums = line.price * (1 - line.contract_discount)

    if line.combination_rule.is_flat_discount:
        return sums - line.combination_rule.combination_discount
    else:
        return sums * (1 - line.combination_rule.combination_discount)


def sum_of_payment(
    base_line: LineDiscount,
    ith: InternatCombination,
    other_line: Union[list[LineDiscount], None] = [],
):
    sums = ith.price
    sums += calculate_contract_contract(base_line)

    for discount in other_line:
        discount_model = LineDiscount(**discount)
        sums += calculate_contract_contract(discount_model)

    return sums


@router.get(
    "/kt/combination",
    summary="combination of KT carrier plan",
    response_description="combination of KT carrier plan",
    response_model=CombinedDiscount,
    # response_model_exclude_unset=True,
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
        combination_rule = fake_combination_rule["single"]
        base_line["combination_rule"] = combination_rule

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
