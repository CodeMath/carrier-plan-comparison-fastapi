from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import Annotated
from typing import Union

from internal.calculater import is_base_line, sum_of_payment
from internal.calculater_range import pay_range_combination, in_range

from dependency import get_db  # SessionLocal()

from combination import combination_crud
from combination.combination_schemas import (
    base_combination_schemas,
)
from db.models import model_combination

from sqlalchemy.orm import Session

from starlette import status


router = APIRouter(
    prefix="/combination",
    tags=["combination"],
    responses={
        404: {"description": "404 not found"},
        403: {"description": "403 Error"},
        400: {"description": "400 Bad request"},
    },
)


@router.post(
    "/create/rule",
    summary="create rule",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def create_combination_rule(
    rule: base_combination_schemas.CreateCombinationRule_Schema,
    db: Session = Depends(get_db),
):
    existing_rule = combination_crud.get_combination_rule_by_name_lines(
        carrier_line=rule.carrier_line, name=rule.name
    )
    if existing_rule:
        raise HTTPException(status_code=409, detail="Already registered")
    combination_crud.create_combination_rule(db=db, rule=rule)


@router.get(
    "/get/rule",
    summary="get rule by id",
    response_model=base_combination_schemas.CombinationRule,
)
async def get_combination_url_by_id(rule_id: int, db: Session = Depends(get_db)):
    result = combination_crud.get_combination_rule_by_id(db=db, rule_id=rule_id)
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="not found")


@router.get(
    "/get/rule",
    summary="get rule by id",
    response_model=base_combination_schemas.CombinationRule,
)
async def get_combination_rule_by_line_name(
    carrier_line: int, name: str, db: Session = Depends(get_db)
):
    result = combination_crud.get_combination_rule_by_name_lines(
        db=db, carrier_line=carrier_line, name=name
    )
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="not found")


@router.post(
    "/single",
    summary="single combination result",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
async def create_single_combination(
    mobile_id: int, internet_id: int, db: Session = Depends(get_db)
):
    is_single_combination_rule = combination_crud.get_combination_rule_by_name_lines(
        db=db, carrier_line=1, name="싱글결합"
    )
    if is_single_combination_rule:
        result = combination_crud.create_combination_single(
            db=db,
            rule_id=is_single_combination_rule.id,
            mobile_id=mobile_id,
            internet_id=internet_id,
        )
        return result
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Already registered"
        )
