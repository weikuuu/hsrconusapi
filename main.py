from fastapi import FastAPI, HTTPException
import uvicorn
from models import LightCone
from data import light_cones


app = FastAPI()


@app.get("/")
def root():
    return {"message": "HSR Light Cone Shelf API"}


@app.get("/light-cones")
def all_light_cones():
    return light_cones


@app.get("/light-cones/{cone_id}")
def get_light_cone(cone_id: int):
    for light_cone in light_cones:
        if light_cone.id == cone_id:
            return light_cone
    raise HTTPException(status_code=404,detail="Light cone not found")


@app.post("/light-cones", status_code=201)
def create_light_cone(light_cone: LightCone):
    for existing_cone in light_cones:
        if existing_cone.id == light_cone.id:
            raise HTTPException(
                status_code=409,
                detail="A light cone with this id already exists"
            )

    light_cones.append(light_cone)
    return light_cone


@app.put("/light-cones/{cone_id}")
def update_light_cone(cone_id: int, updated_cone: LightCone):
    for index, light_cone in enumerate(light_cones):
        if light_cone.id == cone_id:
            light_cones[index] = updated_cone
            return updated_cone
    raise HTTPException(status_code=404,detail="Light cone not found")


@app.delete("/light-cones/{cone_id}")
def delete_light_cone(cone_id: int):
    for index, light_cone in enumerate(light_cones):
        if light_cone.id == cone_id:
            deleted_cone = light_cones.pop(index)

            return {
                "message": "Light cone deleted",
                "light_cone": deleted_cone
            }
    raise HTTPException(status_code=404,detail="Light cone not found")



def main():
    port = 8000

    print(f"HSR API: http://127.0.0.1:{port}/")
    print(f"Light cones: http://127.0.0.1:{port}/light-cones")
    print(f"Site: http://127.0.0.1:{port}/docs")

    uvicorn.run(app, host="127.0.0.1", port=port)


if __name__ == "__main__":
    main()
