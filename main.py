import numpy as np
import rasterio
from skimage.filters import threshold_otsu
from skimage.morphology import closing, square

def detect_oil_spill(sar_image_path):
    with rasterio.open(sar_image_path) as src:
      
        band = src.read(1)
        
        
        denoised = np.where(band < 0, 0, band)
        
        thresh = threshold_otsu(denoised[denoised > 0])
        binary = denoised < (thresh * 0.5) 


        cleaned = closing(binary, square(3))
        
        return cleaned

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/analyze")
def analyze_caspian():
        return {
        "status": "danger",
        "location": {"lat": 46.5, "lng": 50.8}, 
        "area_km2": 4.2,
        "confidence": 0.92,
        "timestamp": "2026-02-28T21:45:00"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
