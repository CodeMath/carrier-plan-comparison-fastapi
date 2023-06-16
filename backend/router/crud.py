from sqlalchemy.orm import Session
from db.models.modle_kt_schemas import *
from db.models.mobile_plan import PlanKT_model
from sqlalchemy import select


def get_plan(db: Session, plan_id: int):
    result = db.query(PlanKT_model).filter(PlanKT_model.id == plan_id).first()
    return result


def get_existing_plan(db: Session, plan: PlanKTinDB):
    result = db.execute(
        select(PlanKT_model).filter(
            (PlanKT_model.title == plan.title)
            | (PlanKT_model.eng_title == plan.eng_title)
        )
    )
    return result.scalars().all()


def get_plan_by_eng_name(db: Session, eng_title: str):
    result = db.query(PlanKT_model).filter(PlanKT_model.eng_title == eng_title).first()
    return result


def get_plan_all(db: Session):
    result = db.query(PlanKT_model).all()
    return result


def create_plan(db: Session, plan: PlanKTinDB):
    db_plan = PlanKT_model(
        title=plan.title,
        eng_title=plan.eng_title,
        price=plan.price,
        carrier=plan.carrier,
        url=plan.url,
    )
    print(db_plan)
    db.add(db_plan)
    db.commit()
