from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True)
    email: str = Field(unique=True)
    password: str
