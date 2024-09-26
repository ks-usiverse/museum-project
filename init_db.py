from database import engine, Base, SessionLocal
from models import Museum

def init_db():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    museum1 = Museum(name="국립중앙박물관", location="서울", description="한국의 대표적인 박물관")
    museum2 = Museum(name="부산시립박물관", location="부산", description="부산의 역사와 문화를 소개")
    session.add_all([museum1, museum2])
    session.commit()
    session.close()

if __name__ == "__main__":
    init_db()