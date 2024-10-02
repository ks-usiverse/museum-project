from database import engine, Base
from sqlalchemy.orm import Session
from models import Museum, Exhibit
import os
import json

def init_db():
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)
    if not session.query(Exhibit).first():
        initial_data_path = os.environ.get('INITIAL_DATA_PATH', 'initial_data.json')
        try:
            with open(initial_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                exhibits = [Exhibit(**item) for item in data]
                session.add_all(exhibits)
                session.commit()
                print("데이터베이스가 로컬 파일을 통해 초기화되었습니다.")
        except FileNotFoundError:
            print(f"초기 데이터 파일을 찾을 수 없습니다: {initial_data_path}")
        except Exception as e:
            print(f"데이터베이스 초기화 중 오류 발생: {e}")
    else:
        print("데이터베이스가 이미 초기화되어 있습니다.")
    session.close()

if __name__ == "__main__":
    init_db()