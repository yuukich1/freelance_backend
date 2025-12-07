from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):

    def to_schema(self):
        pass