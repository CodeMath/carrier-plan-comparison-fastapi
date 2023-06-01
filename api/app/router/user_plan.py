from fastapi import Depends, APIRouter, Header, Query
from typing_extensions import Annotated
from pydantic import Required

from ..internal.planKT import PlanKT, fake_plan, CombinedDiscount
from ..dependency import CarrierPlanQueryParams


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
async def get_items(commons: CarrierPlanQueryParams = Depends(CarrierPlanQueryParams)):
    """
    Get list of KT carrier plan for "가족 프리미엄 결합", "총액결합" and "싱글결합"
    - price: price
    - tp: 5g / LTE / all
    """
    if commons.price:
        ge_plan = []
        for plan in fake_plan:
            if plan["price"] >= commons.price:
                if commons.tp == "all":
                    ge_plan.append(plan)
                elif commons.tp == "5g" and plan["carrier"] == "5G":
                    ge_plan.append(plan)
                elif commons.tp == "LTE" and plan["carrier"] == "LTE":
                    ge_plan.append(plan)

        return ge_plan

    return fake_plan


def is_base_line(plan: list[PlanKT]):
    return min(plan, key=lambda x: x["price"])


@router.get(
    "/kt/combination",
    summary="combination of KT carrier plan",
    response_description="combination of KT carrier plan",
)
async def select_carrier(q: Annotated[list[str], Query(min_lenght=1)] = Required):
    """
    - **q**: each KT plan name
    """
    stored_plan = [plan for plan in fake_plan for name in q if plan["name"] == name]
    # stored_plan_model = list[PlanKT[stored_plan]]

    base_line = is_base_line(stored_plan)

    # single combination
    if len(q) == 1:
        stored_plan[0].update(
            {
                "title": "싱글 결합",
                "contract_discount_25%": base_line["price"] * 0.25,
                "single_contract_discount_25%": base_line["price"] * 0.25,
                "discount_sum": base_line["price"] * 0.5,
                "internet": {
                    "plan": "인터넷 베이직 3년 약정",
                    "mbps": 500,
                    "price": 31350,
                },
                "payment": base_line["price"] * 0.5 + 31350,
            }
        )
    else:
        pass

    # sum_price = 0
    # for splan in stored_plan:
    #     splan.price

    return stored_plan
