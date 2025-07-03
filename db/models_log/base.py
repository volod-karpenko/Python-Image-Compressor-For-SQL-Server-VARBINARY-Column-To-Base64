from db.db_log_config import Base
from sqlalchemy.orm import mapped_column, Mapped

class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column("Id", primary_key=True)

