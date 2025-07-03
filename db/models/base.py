from db.db_config import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import DateTime
import datetime

class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column("Id", primary_key=True)
    CreatedOn: Mapped[datetime.datetime] = mapped_column(DateTime)

