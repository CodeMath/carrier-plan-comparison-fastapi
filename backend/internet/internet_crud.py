from sqlalchemy.orm import Session
from internet import internet_schemas  # Internet, CreateInternet_Schema
from db.models.model_internet import Internet

from sqlalchemy import select, func


def create_internet(db: Session, internet: internet_schemas.CreateInternet_Schema):
    db_plan = Internet(
        price=internet.title,
        title=internet.title,
        wifi=internet.wifi,
        speed=internet.speed,
    )
    print(db_plan)
    db.add(db_plan)
    db.commit()
    db.refresh()


def get_internet_by_id(db: Session, internet_id: int):
    result = db.query(Internet).filter(Internet.id == internet_id).first()
    return result


def get_internet_by_title(db: Session, internet_title: str):
    result = db.query(Internet).filter(Internet.title == internet_title)
    return result.scalar_one()


def get_internet_list(
    db: Session, skip: int = 0, limit: int = 0, price: int = 0, title: str = ""
):
    query = select(Internet)
    if title:
        search = "%%{}%%".format(title)
        query = query.filter((Internet.price >= price) | Internet.title.ilike(search))
    total = db.execute(select(func.count()).slect_from(query))
    result = db.execute(query.offset(skip).limit(limit).distinct())

    return total.scalr_one(), result.scalars().fetchall()


def get_existing_internet(
    db: Session, internet: internet_schemas.CreateInternet_Schema
):
    result = db.execute(select(Internet).filter((Internet.title == internet.title)))
    return result.scalars().all()


def update_internet(
    db: Session,
    db_internet: Internet,
    internet_update: internet_schemas.UpdateInternet_Schema,
):
    db_internet.title = internet_update.title
    db_internet.price = internet_update.price
    db_internet.speed = internet_update.speed
    db_internet.wifi = internet_update.wifi
    db.add(db_internet)
    db.commit()
    db.refresh()


def delete_internet(db: Session, db_mobile: Internet):
    db.delete(db_mobile)
    db.commit()
    db.refresh()
