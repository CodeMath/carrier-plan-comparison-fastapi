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
    SumDiscountCombination,
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
    # response_model=ComparisonPlan,
    # response_model_exclude_unset=True,
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

    except KeyError:
        raise HTTPException(status_code=404)

    try:
        internet = fake_internet[ith]
        base_internet = InternatCombination(**internet)
    except KeyError:
        raise HTTPException(status_code=404)

    # 1) start Plan
    other_line_pay = 0
    for plan in stored_plan:
        other_line_pay += plan["price"]
    result_comparison_plans = ComparisonPlan(
        family_pay=0,
        sum_pay=sum([base_line["price"], other_line_pay]),
        family_plan=None,
        sum_plan=None,
    )
    # 2) check range sum pay
    sums_base_line = base_line
    sums_base_line["contract_discount"] = 0.25
    sums_base_line["combination_rule"] = fake_combination_rule["sums"]

    mobile_plan_list = []

    mobile_plan_list.append(LineDiscount(**sums_base_line))

    for i in stored_plan:
        i["contract_discount"] = 0.25
        i["combination_rule"] = fake_combination_rule["sums"]
        mobile_plan_list.append(LineDiscount(**i))

    # result_comparison_plans.sum_plan
    sum_discout_combination = SumDiscountCombination(
        mobile_plan_list=mobile_plan_list,
        mobile_discount=0,
        internet=base_internet,
        internet_discount=0,
    )
    sum_plans_ith = pay_range_combination(result_comparison_plans.sum_pay)
    if ith.lower() != "slim":
        sum_plan = sum_plans_ith["none-slim"]
    else:
        sum_plan = sum_plans_ith["slim"]

    # check
    if in_range(
        result_comparison_plans.sum_pay,
        sum_plan["mobile_sum_price"][0],
        sum_plan["mobile_sum_price"][1],
    ):
        sum_discout_combination.mobile_discount = sum_plan["mobile_discount"]
        sum_discout_combination.internet_discount = sum_plan["internet_discount"]
        # sum_discout_combination.mobile_plan_list = [base_line, stored_plan]

    result_comparison_plans.sum_plan = sum_discout_combination
    sum_pay_discount_result = (
        (result_comparison_plans.sum_pay * 0.75)
        + base_internet.price
        - sum_plan["mobile_discount"]
        - sum_plan["internet_discount"]
    )
    result_comparison_plans.sum_pay = sum_pay_discount_result

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

    family_combination = CombinedDiscount(
        base_line=base_line_model,
        internet=base_internet,
        other_line=list_of_other_line_model,
        sum_payment=sum_of_payment(
            base_line=base_line_model,
            ith=base_internet,
            other_line=list_of_other_line_model,
        ),
    )

    result_comparison_plans.family_plan = family_combination
    result_comparison_plans.family_pay = family_combination.sum_payment

    return result_comparison_plans
