from typing_extensions import Annotated
from typing import Union

from .modle_kt import (
    PlanKT,
    InternatCombination,
    LineDiscount,
)


def is_base_line(plan: list[PlanKT]):
    return min(plan, key=lambda x: x["price"])


def calculate_contract_contract(line: LineDiscount):
    bill = line.price
    discount_pay = line.price * line.contract_discount

    if line.combination_rule.is_flat_discount:
        return bill - (line.combination_rule.combination_discount + discount_pay)
    else:
        return (
            bill
            - (line.price * line.combination_rule.combination_discount)
            - discount_pay
        )


def sum_of_payment(
    ith: InternatCombination,
    base_line: LineDiscount,
    other_line: Union[list[LineDiscount], None] = [],
):
    sums = ith.price
    base_price = calculate_contract_contract(base_line)
    sums += base_price

    for discount in other_line:
        other_price = calculate_contract_contract(discount)
        sums += other_price
    return sums
