from uuid import UUID

from pydantic import BaseModel, Field


class EstablishmentCreate(BaseModel):
    location: str = Field(..., max_length=50, description="Местоположение заведения")


class EstablishmentUpdate(BaseModel):
    location: str = Field(None, max_length=50, description="Местоположение заведения")


class EstablishmentOut(BaseModel):
    id: UUID
    location: str

    class Config:
        from_attributes = True
