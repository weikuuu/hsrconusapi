from pydantic import BaseModel, Field


class LightCone(BaseModel):
    id: int
    name: str = Field(min_length=1)
    stars: int = Field(ge=3, le=5)
    atk: int = Field(ge=0)
    hp: int = Field(ge=0)
    defense: int = Field(ge=0)
    level: int = Field(ge=1, le=80)
    rank: int = Field(ge=1, le=5)
    description: str | None = None
