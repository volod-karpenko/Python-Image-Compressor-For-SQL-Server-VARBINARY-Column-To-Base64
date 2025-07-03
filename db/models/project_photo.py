from db.models.base import BaseModel
from config import PROJECT_PHOTO_LIMIT_ROWS
from sqlalchemy.orm import mapped_column, Mapped, Session
from sqlalchemy.dialects.mssql import VARBINARY, NVARCHAR, BIT
from sqlalchemy import ScalarResult, or_, and_, select, update, bindparam
from typing import Optional

class ProjectPhoto(BaseModel):
    __tablename__ = "ProjectPhoto"

    MimeType: Mapped[str] = mapped_column(NVARCHAR(128))
    File: Mapped[Optional[bytes]] = mapped_column(VARBINARY())
    Base64PBIStr: Mapped[Optional[str]] = mapped_column(NVARCHAR())
    Base64PBIFlag: Mapped[bool] = mapped_column(BIT)
    Base64PBICompressionRate: Mapped[Optional[int]] = mapped_column()

def get_project_photos(session: Session) -> ScalarResult[ProjectPhoto]:
    image_types = ["jpeg", "jpg", "png"]
    image_types_or_statement = [ProjectPhoto.MimeType.like(f"%{image_type}%") for image_type in image_types]
    return (session.scalars(
              select(ProjectPhoto)
             .where(and_(ProjectPhoto.Base64PBIFlag == False, or_(*image_types_or_statement)))
             .limit(PROJECT_PHOTO_LIMIT_ROWS)
            ))

def update_project_photos(session: Session, photos: list[dict["id": int, "Base64PBIFlag": bool, "Base64PBIStr": str, "Base64PBICompressionRate": Optional[int]]]):
    upd_query = (
        update(ProjectPhoto)
        .where(ProjectPhoto.id == bindparam("id"))
        .values(Base64PBIFlag = bindparam("Base64PBIFlag"),
                Base64PBIStr = bindparam("Base64PBIStr"),
                Base64PBICompressionRate = bindparam("Base64PBICompressionRate"))
        .execution_options(synchronize_session=None)
    )
    step = 10
    for i in range(0, len(photos), step):
        session.execute(upd_query, photos[i:i+step])
        session.commit()