import os
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not defined!")

engine = create_engine(
    url=DATABASE_URL
)

session = sessionmaker(engine, expire_on_commit=False)


def get_db() -> Session:
    db = session()
    try:
        yield db
    finally:
        db.close()


class Base(DeclarativeBase):
    pass


def redis_test_con():
    r = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=os.getenv('REDIS_DB'),
                    username=os.getenv('REDIS_USER'), password=os.getenv('REDIS_PASSWORD'))
    try:
        info = r.info()
        print(info['redis_version'])
        response = r.ping()
        if response:
            print("Connection success!")
        else:
            print("Can't connect to redis db.")
    except redis.exceptions.RedisError as e:
        print(f"ERROR: {e}")
