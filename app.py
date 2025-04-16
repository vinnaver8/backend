from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import requests
import base64
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = "https://api-inference.huggingface.co/models/hysts/anime-stylegan2"
HF_TOKEN = "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"  # <-- Replace with your Hugging Face token

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

@app.get("/")
def home():
    return {"message": "Anime StyleGAN2 API is working!"}

@app.post("/generate")
async def generate(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file).convert("RGB")
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_bytes = buffered.getvalue()

        response = requests.post(API_URL, headers=headers, data=img_bytes)
        if response.status_code != 200:
            return {"error": response.json()}

        # Convert binary to base64 string
        base64_img = base64.b64encode(response.content).decode("utf-8")
        return {"output_base64": base64_img}

    except Exception as e:
        return {"error": str(e)}
