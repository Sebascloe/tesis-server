from fastapi import File, UploadFile, APIRouter
from pathlib import Path
from PIL import Image
from io import BytesIO

router = APIRouter()

UPLOAD_FOLDER = Path("./images")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


def convert_and_save_image(image_data: bytes, filename: str, save_path: Path):
    with Image.open(BytesIO(image_data)) as img:
        img = img.convert("RGBA")

        img.save(save_path.with_suffix(".png"), format="PNG")


@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    if file.content_type.startswith("image/"):
        image_data = await file.read()

        file_location = UPLOAD_FOLDER / file.filename

        convert_and_save_image(image_data, file.filename, file_location)

        return {
            "message": f"Image successfully uploaded and converted to PNG at {file_location.with_suffix('.png')}"
        }
    else:
        return {"error": "The uploaded file is not an image."}
