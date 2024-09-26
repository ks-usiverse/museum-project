from pydantic import BaseModel

class MuseumSchema(BaseModel):
    id: int
    name: str
    location: str
    description: str

    class Config:
        orm_mode = True