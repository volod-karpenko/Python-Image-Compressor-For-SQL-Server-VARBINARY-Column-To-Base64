# :camera: Python Image Compressor -> Compresses Image From VARBINARY SQL Server Column To Base64 Of A Specified Length

## :bulb: The Motivation Behind The Project
Recently I've been a part of the team developing :chart_with_upwards_trend: **Power BI** reports for a non-called government service which wanted to have some analytics about its restoration & building projects.  
:see_no_evil: The customer was very persistent about drilling-through to a selected project to view the data & **images** of the project on a separate page.  
:mag_right: Inside the box, the data was stored in SQL Server Database in two tables (indeed there were much more tables but it's enough to remark only these two):
- **Project**
- **ProjectPhoto** 
    - **Id**
    - **Project_Id**
    - **File** *VARBINARY*
    - **FileShort** *NVARCHAR of base64*
    - **MimeType**

:thought_balloon: At first, **FileShort** column was used to display the images in **Power BI** reports but soon we bumped into two problems:
- **FileShort** was too much compressed & the quality could be better
- **Power BI** has the upper bound for text columns of **32k** symbols & truncates the overflow, so if **FileShort** was more than 32k symbols the image would be truncated  
Originally, **FileShort** column has been developed for a very different purpose - to display a compressed preview of the image in the gallery & there it did its best :point_down:
![FileShort Column Purposed Usage](https://i.postimg.cc/ht8G6qtH/file-short-column-usage.png)

### :raised_hands: There the idea of a separate process that would generate *power-bi-purposed* base64 & save it into a new column came to my mind
**Project Photo** new columns:
1. **Base64PBIStr** -> new column to store base64 for **Power BI** purpose
2. **Base64PBIFlag** -> to mark if the image has been processed, if so - don't process it again
3. **Base64PBICompressionRate** -> to store compression rate (between 5% and 99%), the **lower** the value the **better** quality has been preserved

## :rocket: Results Achieved
1. Better quality for most of the images: on average for each image **the length of the base64 string has grown twice**, so did the quality :point_down:  
![better-quality-example-1.png](https://i.postimg.cc/sDMsdGVF/better-quality-example-1.png)  
![better-quality-example-2.png](https://i.postimg.cc/Pqjjw61h/better-quality-example-2.png)  
![better-quality-example-3.png](https://i.postimg.cc/K8Lb4XkJ/better-quality-example-3.png)  
2. Truncated images aren't truncated anymore :point_down:  
![truncation-example-1.png](https://i.postimg.cc/KvCFZcz1/truncation-example-1.png)  
![truncation-example-2.png](https://i.postimg.cc/yNyzXFTR/truncation-example-2.png)  
![truncation-example-3.png](https://i.postimg.cc/NMkZmBBk/truncation-example-3.png)  

## :file_folder: Project Structure
<pre>
root/
├─ config/
│  ├─ __init__.py
│  ├─ load_config.py
├─ db/
│  ├─ models/
│  │  ├─ __init__.py
│  │  ├─ base.py
│  │  ├─ project_photo.py
│  ├─ models_log/
│  │  ├─ __init__.py
│  │  ├─ base.py
│  │  ├─ integration_history.py
│  │  ├─ status_enum.py
│  ├─ db_config.py
│  ├─ db_log_config.py
├─ image/
│  ├─ __init__.py
│  ├─ methods.py
├─ log/
│  ├─ __init__.py
│  ├─ setup.py
├─ .gitignore
├─ main.py
├─ README.md
├─ requirements.txt
</pre>

## :electric_plug: Installation Instructions (Windows)
```bash
git clone https://github.com/volod-karpenko/Python-Image-Compressor-For-SQL-Server-VARBINARY-Column-To-Base64.git
cd Python-Image-Compressor-For-SQL-Server-VARBINARY-Column-To-Base64
python -m venv venv
pip install -r requirements.txt
```
These commands clone the repository, change the directory to the root folder of ```main.py```, initialize python virtual environment for the project & install the libraries.   
After you configure the ```.env``` file & set up databases ([you can download minimum necessary database backups here - image binary sample data included](https://drive.google.com/file/d/15pEfpQGgYW7dfX_VEQVyf7wQ1biWyX-G/view?usp=sharing)), go to ```Python-Image-Compressor-For-SQL-Server-VARBINARY-Column-To-Base64``` folder & run in cmd:
```bash
venv\Scripts\activate
python main.py
```
:bookmark: I personally created ```.bat``` file & configured a task in **Task Scheduler** to run the script automatically on a schedule

## :hammer_and_wrench: Libraries Used
- ```SQLAlchemy``` (ORM) -> to query database data
- ```Pillow``` -> to work with images
- ```logging``` -> to log to ```logs.log```
- ```dotenv``` -> to load ```.env```
- ```base64```, ```io``` -> to work with base64 & in-memory buffer

## :nail_care: Environment Variables
Most of the **configuration variables** are taken out to ```.env``` (go to ```load_config.py``` to examine in depth)  
Here is a comprehensive list of them:
- :exclamation: **DATABASE_URL** -> connection url to SQL Server *Photo* Database, **requiered**
- :exclamation: **DATABASE_LOG_URL** -> connection url to SQL Server *HISTORY* Database, **requiered** in case you set ```DATABASE_LOG_FLAG = 1```
- :grey_exclamation: **PROJECT_PHOTO_LIMIT_ROWS** -> number of photos that are processed within one program run, **optional**, ```default = 25```
- :exclamation: **INTEGRATION_TYPE_ID** -> is necessary for the legacy *HISTORY* Database structure , **requiered** in case you set ```DATABASE_LOG_FLAG = 1```
- :grey_exclamation: **DATABASE_LOG_FLAG** -> specifies if logs are written to *HISTORY* Database, **optional**, ```default = 0```
- :grey_exclamation: **INFO_LOG** -> specifies if logs are written to *logs.log*, **optional**, ```default = 0```
- :grey_exclamation: **ERROR_MESSAGE** -> custom error message to write to *HISTORY* Database, **optional**, ```default = "Oooppppsssss...unexpected error occured! Please, examine program logs for more details"```
- :grey_exclamation: **BASE64_STRING_LENGTH** -> the upper bound of a *base64* string length, **optional**, ```default = 32000```  
As for the database logs, you may turn them off, but I needed them to monitor in the main system if the **Task Scheduler** successfully runs the script & process the images :point_down:
![history-logs.png](https://i.postimg.cc/ZKn3GHBT/history-logs.png)

## :no_entry_sign: Limitations
1. Only **jpeg**, **jpg**, **png** are processed
2. There is a set of attempts to compress the image and check the corresponding base64 string length, the last attempt compresses to **1%** of the original size - if base64 string length is still *>=32k symbols* the image is marked as processed but **Base64PBIStr** is set to ```NULL```

## :eyes: Code Preview
- preview of **ProjectPhoto** table structure:
```python
class ProjectPhoto(BaseModel):
    __tablename__ = "ProjectPhoto"

    MimeType: Mapped[str] = mapped_column(NVARCHAR(128))
    File: Mapped[Optional[bytes]] = mapped_column(VARBINARY())
    Base64PBIStr: Mapped[Optional[str]] = mapped_column(NVARCHAR())
    Base64PBIFlag: Mapped[bool] = mapped_column(BIT)
    Base64PBICompressionRate: Mapped[Optional[int]] = mapped_column()
```  

- preview of **IntegrationHistory** table structure:
```python
class IntegrationHistory(BaseModel):
    __tablename__ = "IntegrationHistory"

    IntegrationStatus_Id: Mapped[int] = mapped_column(TINYINT)
    IntegrationType_Id: Mapped[int] = mapped_column(TINYINT)
    StartDate: Mapped[datetime.datetime] = mapped_column(DateTime)
    EndDate: Mapped[datetime.datetime] = mapped_column(DateTime)
    ErrorMessage: Mapped[Optional[str]] = mapped_column(NVARCHAR(4000))
    SPID: Mapped[int] = mapped_column()
    Details: Mapped[Optional[str]] = mapped_column(NVARCHAR(4000))
```  

- preview of **image methods** (```image\methods.py```):
```python
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
```

## :raising_hand_man: Author
Volodymyr Karpenko  
[LinkedIn](https://www.linkedin.com/in/volod-karpenko/) • <a href="mailto:volod1701@gmail.com">Email </a>(volod1701@gmail.com)