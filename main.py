from fastapi import Depends, FastAPI, HTTPException
import uvicorn
from models import LightCone
from database import Base, engine, get_db
from sqlalchemy.orm import Session
import db_models


app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "HSR Light Cone Shelf API"}


@app.get("/light-cones")
def get_light_cones(db: Session = Depends(get_db)):
    return db.query(db_models.LightConeDB).all()


@app.get("/light-cones/{cone_id}")
def get_light_cone(
    cone_id: int,
    db: Session = Depends(get_db),
):
    cone = (
        db.query(db_models.LightConeDB)
        .filter(db_models.LightConeDB.id == cone_id)
        .first()
    )

    if cone is None:
        raise HTTPException(
            status_code=404,
            detail="Light cone not found",
        )

    return cone


@app.post("/light-cones", status_code=201)
def create_light_cone(
    new_cone: LightCone,
    db: Session = Depends(get_db),
):
    existing_cone = (
        db.query(db_models.LightConeDB)
        .filter(db_models.LightConeDB.id == new_cone.id)
        .first()
    )

    if existing_cone:
        raise HTTPException(
            status_code=409,
            detail="Light cone with this id already exists",
        )

    db_cone = db_models.LightConeDB(**new_cone.model_dump())

    db.add(db_cone)
    db.commit()
    db.refresh(db_cone)

    return db_cone


@app.put("/light-cones/{cone_id}")
def update_light_cone(
    cone_id: int,
    updated_cone: LightCone,
    db: Session = Depends(get_db),
):
    cone = (
        db.query(db_models.LightConeDB)
        .filter(db_models.LightConeDB.id == cone_id)
        .first()
    )

    if cone is None:
        raise HTTPException(
            status_code=404,
            detail="Light cone not found",
        )

    if updated_cone.id != cone_id:
        raise HTTPException(
            status_code=400,
            detail="Path id and body id must match",
        )

    for field, value in updated_cone.model_dump().items():
        setattr(cone, field, value)

    db.commit()
    db.refresh(cone)

    return cone


@app.delete("/light-cones/{cone_id}")
def delete_light_cone(
    cone_id: int,
    db: Session = Depends(get_db),
):
    cone = (
        db.query(db_models.LightConeDB)
        .filter(db_models.LightConeDB.id == cone_id)
        .first()
    )

    if cone is None:
        raise HTTPException(
            status_code=404,
            detail="Light cone not found",
        )

    db.delete(cone)
    db.commit()

    return {"message": "Light cone deleted"}



def main():
    port = 8000

    print(f"HSR API: http://127.0.0.1:{port}/")
    print(f"Light cones: http://127.0.0.1:{port}/light-cones")
    print(f"Site: http://127.0.0.1:{port}/docs")

    uvicorn.run(app, host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
