import logging
from log import *
setup_logger()
logger = logging.getLogger(__name__)

from config import DATABASE_LOG_FLAG, INFO_LOG, ERROR_MESSAGE
from db.db_config import get_db_session
from db.models import get_project_photos, update_project_photos
from image import resize_to_base64
from datetime import datetime, timezone

def resize_photos(session):
    compressed_photos_count = 0
    all_photos_count = 0
    resized_photos = []
    for photo in get_project_photos(session=session):
        resized_photo = { "id": photo.id, "Base64PBIFlag": True, "Base64PBIStr": None, "Base64PBICompressionRate": None }
        try:
            compression_rate, base64str = resize_to_base64(photo.File)
            if compression_rate != None: compressed_photos_count = compressed_photos_count + 1
            resized_photo["Base64PBICompressionRate"] = compression_rate
            resized_photo["Base64PBIStr"] = base64str
        except:
            continue
        finally:
            resized_photos.append(resized_photo)
            all_photos_count = all_photos_count + 1
    return (resized_photos, all_photos_count, compressed_photos_count)

ok = True
error_message = None
start_time = datetime.now(timezone.utc)
all_photos_count = 0
compressed_photos_count = 0

for session in get_db_session():
    try:
        if session == None: raise Exception("database session is corrupted. Examine db_config.py & logs above to learn more!")
        photos, all_photos_count, compressed_photos_count = resize_photos(session=session)
        update_project_photos(session=session, photos=photos)
        if INFO_LOG: logger.info(f"Successfully processed {compressed_photos_count}/{all_photos_count} images")
    except Exception as error:
        ok = False
        error_message = ERROR_MESSAGE
        logger.error(f"Error while resizing photos: {error}")

end_time = datetime.now(timezone.utc)

if DATABASE_LOG_FLAG > 0:
    try:
        from db.models_log import *
        status = IntegrationStatus.SUCCESSFUL if ok else IntegrationStatus.FAILED
        details = f"Успішно опрацьовано {compressed_photos_count}/{all_photos_count} зображень 😀"
        id = insert_integration_history_row(status=status, start_time=start_time, end_time=end_time, error_message=error_message, details=details)
        if INFO_LOG: logger.info(f"Database log with id={id} successfully inserted")
    except Exception as error:
        logger.error(f"Error while creating a database log: {error}")