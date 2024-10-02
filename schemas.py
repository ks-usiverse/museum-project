from pydantic import BaseModel

class MuseumSchema(BaseModel):
    id: int
    name: str
    location: str
    description: str

    class Config:
        orm_mode = True

class ExhibitSchema(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True