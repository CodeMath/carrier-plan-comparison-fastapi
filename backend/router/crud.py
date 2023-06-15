from sqlalchemy.orm import Session
from db.models.modle_kt_schemas import *
from db.models.mobile_plan import PlanKT_model


def get_plan(db: Session, plan_id: int):
    return db.query(PlanKT_model).filter(PlanKT_model.id == plan_id).frist()


def get_plan_by_ko_name(db: Session, title: str):
    return db.query(PlanKT_model).filter(PlanKT_model.title == title).frist()


def get_plan_by_eng_name(db: Session, eng_title: str):
    return db.query(PlanKT_model).filter(PlanKT_model.eng_title == eng_title).frist()


def get_first_plan(db: Session):
    return db.query(PlanKT_model).first()


def create_plan(db: Session, plan: PlanKTinDB):
    db_plan = PlanKT_model(**plan.dict())
    db.add(db_plan)
    db.refresh(db_plan)
    return db_plan
