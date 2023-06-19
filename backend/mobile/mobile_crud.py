from sqlalchemy.orm import Session
from mobile import mobile_schemas  # Mobile, CreateMobile_Schema

from db.models.model_mobile import Mobile

from sqlalchemy import select, func


def create_mobile(db: Session, mobile: mobile_schemas.CreateMobile_Schema):
    db_plan = Mobile(
        plan=mobile.plan,
        price=mobile.price,
        carrier=mobile.carrier,
        url=mobile.url,
    )
    print(db_plan)
    db.add(db_plan)
    db.commit()
    db.refresh()


def get_mobile_by_id(db: Session, mobile_id: int):
    result = db.query(Mobile).filter(Mobile.id == mobile_id).first()
    return result


def get_mobile_by_title(db: Session, mobile_plan: str):
    result = db.query(Mobile).filter(Mobile.plan == mobile_plan)
    return result.scalar_one()


def get_mobile_list(
    db: Session, skip: int = 0, limit: int = 0, price: int = 0, carrier: str = ""
):
    query = select(Mobile)
    if carrier:
        search = "%%{}%%".format(carrier)
        query = query.filter((Mobile.plan >= price) | Mobile.carrier.ilike(search))
    total = db.execute(select(func.count()).slect_from(query))
    result = db.execute(query.offset(skip).limit(limit).distinct())

    return total.scalr_one(), result.scalars().fetchall()


def get_existing_mobile(db: Session, mobile: mobile_schemas.CreateMobile_Schema):
    result = db.execute(select(Mobile).filter((Mobile.plan == mobile.plan)))
    return result.scalars().all()


def update_mobile(
    db: Session,
    db_mobile: Mobile,
    mobile_update: mobile_schemas.UpdateMobile_Schema,
):
    db_mobile.plan = mobile_update.plan
    db_mobile.price = mobile_update.price
    db_mobile.url = mobile_update.url
    db_mobile.carrier = mobile_update.carrier
    db.add(db_mobile)
    db.commit()
    db.refresh()


def delete_mobile(db: Session, db_mobile: Mobile):
    db.delete(db_mobile)
    db.commit()
    db.refresh()
