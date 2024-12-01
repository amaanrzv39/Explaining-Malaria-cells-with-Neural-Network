from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from PIL import Image
import base64
from io import BytesIO
from model import prediction


# Create FastAPI app
app = FastAPI()

# Set up templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


def encode_image_to_base64(img: Image.Image) -> str:
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


# Prediction endpoint
@app.post("/predict/")
async def predict_image(request:Request, file: UploadFile = File(...)):
    # Preprocess image
    image_bytes = await file.read()
    img = Image.open(BytesIO(image_bytes))
    
    # Get the prediction
    predicted_class, score, gradcam_output = await prediction(img)
    
    gradcam_img = encode_image_to_base64(gradcam_output)
    encoded_image = encode_image_to_base64(img)

    return templates.TemplateResponse(
                "result.html", {"request":request,
                            "prediction_score":score if predicted_class==1 else 1-score, 
                            "prediction": "Malaria" if predicted_class==0 else "Normal", 
                            "image":encoded_image,
                            "grid":gradcam_img}
        )


# Main page
@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})