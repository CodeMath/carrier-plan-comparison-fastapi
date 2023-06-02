from typing_extensions import Annotated
from typing import Union

from ..internal.planKT import (
    PlanKT,
    InternatCombination,
    LineDiscount,
)


def is_base_line(plan: list[PlanKT]):
    return min(plan, key=lambda x: x["price"])


def calculate_contract_contract(line_model: LineDiscount):
    line = LineDiscount(**line_model)
    sums = line.price * (1 - line.contract_discount)

    if line.combination_rule.is_flat_discount:
        return sums - line.combination_rule.combination_discount
    else:
        return sums - (line.price * line.combination_rule.combination_discount)


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
