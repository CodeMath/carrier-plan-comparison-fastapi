from sqlalchemy.orm import Session
from sqlalchemy import select
from combination.combination_schemas import (
    base_combination_schemas,
    product_combination_schemas,
)
from mobile.mobile_schemas import CreateMobile_Schema

from db.models.model_mobile import Mobile
from db.models.model_internet import Internet
from db.models.model_combination import CombinationRule, CombinationSingle
from db.models.model_result import ResultBoard


from datetime import datetime
from typing import List

from mobile.mobile_crud import get_mobile_by_id
from internet.internet_crud import get_internet_by_id


# 결합 룰 생성
def create_combination_rule(
    db: Session, rule: base_combination_schemas.CreateCombinationRule_Schema
):
    result = CombinationRule(
        name=rule.name,
        carrier_line=rule.carrier_line,
        is_flat_discount=rule.is_flat_discount,
        combination_discount=rule.combination_discount,
    )
    db.add(result)
    db.commit


# 결합 룰 선택: 회선 수, name
def get_combination_rule_by_name_lines(db: Session, carrier_line: int, name: str):
    rule = db.execute(
        select(CombinationRule).filter(
            (CombinationRule.carrier_line == carrier_line)
            & (CombinationRule.name == name)
        )
    )
    return rule.scalar_one()


# 결합 룰 선택: id
def get_combination_rule_by_id(db: Session, rule_id: int):
    return db.query(CombinationRule).filter(CombinationRule.id == rule_id).scalar_one()


def create_mobile_discount(
    db: Session, rule_id: int, mobile: CreateMobile_Schema
) -> base_combination_schemas.CreateLineDiscount_Schema:
    get_combination_rule_db = get_combination_rule_by_id(db=db, rule_id=rule_id)

    mobile_pay = mobile.price - (mobile.price * 0.25)

    if get_combination_rule_db.is_flat_discount:
        mobile_pay -= get_combination_rule_db.combination_discount
    else:
        mobile_pay -= mobile.price * get_combination_rule_db.combination_discount

    mapped_line_discount = {
        "combination_rule": get_combination_rule_db,
        "contract_discount": 0.25,
        "mobile": mobile,
        "mobile_pay": mobile_pay,
    }

    return base_combination_schemas.CreateLineDiscount_Schema(**mapped_line_discount)


# 싱글 결합 시, 수정필요
def create_combination_single(
    db: Session, rule_id: int, mobile_id: int, internet_id: int
):
    get_rule_db = get_combination_rule_by_id(db=db, rule_id=rule_id)
    get_mobile_db = get_mobile_by_id(db=db, mobile_id=mobile_id)
    get_internet_db = get_internet_by_id(db=db, internet_id=internet_id)

    get_line_discount_schema = create_mobile_discount(
        db=db, rule_id=rule_id, internet_id=get_internet_db.id, mobile=get_mobile_db
    )
    CombinationSingle(
        create_time=datetime.now(),
        base_line_id=get_mobile_db,
        internet_id=get_internet_db,
        sum_payment=get_line_discount_schema.mobile_pay + get_internet_db.price,
    )
    intial_price = get_mobile_db.price + get_internet_db.price

    # discount by rule: flat
    discount_sum = 0
    if get_rule_db.is_flat_discount:
        discount_sum += get_rule_db.combination_discount
    else:
        discount_sum = get_mobile_db.price * get_rule_db.combination_discount

    single_result = ResultBoard(
        create_time=datetime.now(),
        combination_rule=get_rule_db,
        # combination_rule_id=get_rule_db.id,
        title=get_rule_db.name,
        initial_price=intial_price,
        discount_price=discount_sum,
        result_price=intial_price - discount_sum,
        # mobile_id=get_mobile_db.id,
        # internet_id=get_internet_db.id,
        other_mobile=None,
        mobile=get_mobile_db,
        Internet=get_internet_db,
    )
    db.add(single_result)
    db.commit()

    return single_result


# 가족 결합 시, 수정필요.
def create_combination_family(
    db: Session,
    rule_id: int,
    family_plan: product_combination_schemas.CreateCombination_Schema,
):
    get_rule_db = get_combination_rule_by_id(db=db, rule_id=rule_id)

    intial_price = get_mobile_db.price + get_internet_db.price

    # discount by rule: flat
    discount_sum = 0
    if get_rule_db.is_flat_discount:
        discount_sum += get_rule_db.combination_discount
    else:
        discount_sum = get_mobile_db.price * get_rule_db.combination_discount

    ResultBoard(
        create_time=datetime.now(),
        combination_rule=get_rule_db,
        # combination_rule_id=get_rule_db.id,
        title=get_rule_db.name,
        initial_price=intial_price,
        discount_price=discount_sum,
        result_price=intial_price - discount_sum,
        # mobile_id=get_mobile_db.id,
        # internet_id=get_internet_db.id,
        other_mobile=None,
        mobile=get_mobile_db,
        Internet=get_internet_db,
    )
