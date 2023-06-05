from fastapi import APIRouter, Query, HTTPException
from typing_extensions import Annotated
from typing import Union
from ..internal.calculater import is_base_line, sum_of_payment
from ..internal.calculater_range import pay_range_combination, in_range

from ..internal.modle_kt import (
    InternatCombination,
    CombinedDiscount,
    LineDiscount,
    ComparisonPlan,
)

from ..fake_db.fake_db import fake_plan, fake_internet, fake_combination_rule


router = APIRouter(
    prefix="/combination",
    tags=["combination"],
    responses={404: {"description": "404 not found"}},
)


@router.get(
    "/kt",
    summary="combination of KT carrier plan: Family, Single Combination",
    response_description="combination of KT carrier plan: Family, Single Combination",
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
        stored_plan.remove(base_line)
        other_line = stored_plan
        print(base_line)
        print(other_line)
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
            sum_payment=sum_of_payment(base_line=base_line_model, ith=base_internet),
        )
        return single_combination
    else:
        # check 2 case
        base_combination_rule = fake_combination_rule["family_base"]
        other_combination_rule = fake_combination_rule["family_other"]

        base_line["combination_rule"] = base_combination_rule
        base_line["contract_discount"] = 0.25
        base_line_model = LineDiscount(**base_line)

        list_of_other_line_model = []
        for line in other_line:
            line["combination_rule"] = other_combination_rule
            line["contract_discount"] = 0.25
            list_of_other_line_model.append(LineDiscount(**line))

        result_combination = CombinedDiscount(
            base_line=base_line_model,
            internet=base_internet,
            other_line=list_of_other_line_model,
            sum_payment=sum_of_payment(
                base_line=base_line_model,
                ith=base_internet,
                other_line=list_of_other_line_model,
            ),
        )
        return result_combination


@router.get(
    "/kt/between",
    summary="Comparison of Family and Sum plan",
    response_description="Comparison of Family and Sum plan",
    response_model=ComparisonPlan,
    response_model_exclude_unset=True,
)
async def comparison_plan(
    q: Annotated[
        Union[list[str], None],
        Query(
            min_lenght=1,
            examples=fake_plan,
        ),
    ],
    ith: Annotated[str, Query(examples=fake_internet)],
):
    try:
        stored_plan = [fake_plan[name] for name in q]
        base_line = is_base_line(stored_plan)
        stored_plan.remove(base_line)
        other_line = stored_plan
        print(base_line)
        print(other_line)
    except KeyError:
        raise HTTPException(status_code=404)

    try:
        internet = fake_internet[ith]
        base_internet = InternatCombination(**internet)
    except KeyError:
        raise HTTPException(status_code=404)
    # 1) start Plan

    comparison_plans = ComparisonPlan(
        family_pay=0,
        sum_pay=sum(
            [
                price[1]
                for plan in stored_plan.items()
                for price in plan
                if price[0] == "price"
            ]
        ),
        family_plan=None,
        sum_plan=None,
    )
    # 2) check range sum pay

    sum_plans_ith = pay_range_combination(comparison_plans.sum_pay)
    if ith.lower() != "slim":
        sum_plan = sum_plans_ith["none-slim"]
    else:
        sum_plan = sum_plans_ith["slim"]

    # check
    if in_range(
        comparison_plans.sum_pay,
        sum_plan["mobile_sum_price"][0],
        sum_plan["mobile_sum_price"][1],
    ):
        sum_plan["mobile_discount"]
        sum_plan["internet_discount"]
        comparison_plans.sum_plan = 0

    # 3) get Family Plans

    base_combination_rule = fake_combination_rule["family_base"]
    other_combination_rule = fake_combination_rule["family_other"]

    base_line["combination_rule"] = base_combination_rule
    base_line["contract_discount"] = 0.25
    base_line_model = LineDiscount(**base_line)

    list_of_other_line_model = []
    for line in other_line:
        line["combination_rule"] = other_combination_rule
        line["contract_discount"] = 0.25
        list_of_other_line_model.append(LineDiscount(**line))

    result_combination = CombinedDiscount(
        base_line=base_line_model,
        internet=base_internet,
        other_line=list_of_other_line_model,
        sum_payment=sum_of_payment(
            base_line=base_line_model,
            ith=base_internet,
            other_line=list_of_other_line_model,
        ),
    )

    return comparison_plans
