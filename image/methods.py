from config import BASE64_STRING_LENGTH
from PIL import Image
import base64
import io
from typing import Optional

def bytes_to_image(binary_file: bytes) -> Optional[Image.Image]:
    try:
        with io.BytesIO(binary_file) as buffer:
            image = Image.open(buffer)
            image.load()
            if image.mode != "RGB": image = image.convert("RGB")
            return image
    except:
        return None
    
def resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    return image.resize(size, Image.Resampling.LANCZOS)

def convert_to_base64(image: Image.Image) -> str:
    with io.BytesIO() as buffer:
        image.save(buffer, format="JPEG", optimize=True)
        iobytes = buffer.getvalue()
        base64str = base64.b64encode(iobytes).decode("utf-8")
        return base64str
    
def resize_to_base64(binary_file: bytes, base64str_length_limit = BASE64_STRING_LENGTH) -> tuple[Optional[int], str]:
    image = bytes_to_image(binary_file=binary_file)
    if not image:
        return (None, "")
    compression_rate_list = [95, 85, 75, 65, 55, 45, 35, 25, 20, 15, 10, 5, 4, 3, 2, 1]
    for compression_rate in compression_rate_list:
        new_size = (int(size * compression_rate / 100) for size in image.size)
        resized_image = resize(image=image, size=new_size)
        base64str = convert_to_base64(image=resized_image)
        if len(base64str) < base64str_length_limit:
            return (100 - compression_rate, base64str)
        
    return (None, "")
