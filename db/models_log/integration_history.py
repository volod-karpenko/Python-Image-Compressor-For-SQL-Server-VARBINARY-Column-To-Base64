from config import INTEGRATION_TYPE_ID
from db.db_log_config import get_log_db_session
from .base import BaseModel
from sqlalchemy import DateTime, insert
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.mssql import TINYINT, NVARCHAR
from typing import Optional
from .status_enum import IntegrationStatus
import datetime

class IntegrationHistory(BaseModel):
    __tablename__ = "IntegrationHistory"

    IntegrationStatus_Id: Mapped[int] = mapped_column(TINYINT)
    IntegrationType_Id: Mapped[int] = mapped_column(TINYINT)
    StartDate: Mapped[datetime.datetime] = mapped_column(DateTime)
    EndDate: Mapped[datetime.datetime] = mapped_column(DateTime)
    ErrorMessage: Mapped[Optional[str]] = mapped_column(NVARCHAR(4000))
    SPID: Mapped[int] = mapped_column()
    Details: Mapped[Optional[str]] = mapped_column(NVARCHAR(4000))

def insert_integration_history_row(status: IntegrationStatus, start_time: datetime.datetime, end_time: datetime.datetime, error_message: str | None = None, details: str | None = None) -> int:
    if INTEGRATION_TYPE_ID == None: raise Exception("INTEGRATION_TYPE_ID is not set properly!")

    query = insert(IntegrationHistory).values(
        IntegrationType_Id = INTEGRATION_TYPE_ID,
        IntegrationStatus_Id = status.value,
        StartDate = start_time,
        EndDate = end_time,
        ErrorMessage = error_message[0:4000] if error_message and status == IntegrationStatus.FAILED else None,
        SPID = 0,
        Details = details[0:4000] if details else None
    ).returning(IntegrationHistory.id)

    for session in get_log_db_session():
        if session == None: raise Exception("log database session is corrupted. Examine db_log_config.py & logs above to learn more!")
        id = session.scalars(query).first()
        session.commit()
        return id

