from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from gradio_client import Client, handle_file
from PIL import Image
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Fluxen Ghibli API is working. Use POST /generate"}

@app.post("/generate")
async def generate(file: UploadFile = File(...)):
    try:
        image = Image.open(file.file).convert("RGB")
        temp_path = "/tmp/temp_input.png"
        image.save(temp_path)

        client = Client("jamesliu1217/EasyControl_Ghibli")
        result = client.predict(
            prompt="Ghibli Studio style, Charming hand-drawn anime-style illustration",
            spatial_img=handle_file(temp_path),
            height=768,
            width=768,
            seed=42,
            control_type="Ghibli",
            use_zero_init=False,
            zero_steps=1,
            api_name="/single_condition_generate_image"
        )

        return {"output_url": result}

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
