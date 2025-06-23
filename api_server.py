from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import json
import numpy as np
from typing import List

# Crear aplicación FastAPI
app = FastAPI(
    title="API Predicción Precios de Casas",
    description="API para predecir precios de viviendas usando Machine Learning",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class HouseFeatures(BaseModel):
    area_m2: float
    habitaciones: int
    baños: int
    antiguedad: int
    distancia_centro: float
    garaje: int  # 0 o 1
    jardin: int  # 0 o 1

class PredictionResponse(BaseModel):
    precio_predicho: float
    precio_formateado: str
    caracteristicas_enviadas: dict

class ModelMetrics(BaseModel):
    mae_test: float
    r2_test: float
    rmse_test: float
    n_samples: int
    features: List[str]

# Cargar modelo y métricas al iniciar
try:
    model = joblib.load('house_price_model.pkl')
    with open('model_metrics.json', 'r') as f:
        metrics_data = json.load(f)
    print("Modelo cargado correctamente")
except FileNotFoundError:
    print("Error: Archivos del modelo no encontrados. Ejecuta primero train_house_price_model.py")
    model = None
    metrics_data = None

@app.get("/")
async def root():
    return {
        "mensaje": "API de Predicción de Precios de Casas",
        "version": "1.0.0",
        "estado": "activo" if model else "modelo no cargado",
        "endpoints": [
            "/predict - Realizar predicción",
            "/metrics - Ver métricas del modelo",
            "/health - Estado de la API"
        ]
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_price(features: HouseFeatures):
    if model is None:
        raise HTTPException(status_code=503, detail="Modelo no disponible")
    
    try:
        # Convertir a formato numpy
        input_data = np.array([[
            features.area_m2,
            features.habitaciones,
            features.baños,
            features.antiguedad,
            features.distancia_centro,
            features.garaje,
            features.jardin
        ]])
        
        # Realizar predicción
        prediction = model.predict(input_data)[0]
        
        # Formatear respuesta
        return PredictionResponse(
            precio_predicho=float(prediction),
            precio_formateado=f"${prediction:,.2f}",
            caracteristicas_enviadas=features.dict()
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error en predicción: {str(e)}")

@app.get("/metrics", response_model=ModelMetrics)
async def get_model_metrics():
    if metrics_data is None:
        raise HTTPException(status_code=503, detail="Métricas no disponibles")
    
    return ModelMetrics(**metrics_data)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if model else "unhealthy",
        "modelo_cargado": model is not None,
        "metricas_disponibles": metrics_data is not None
    }

@app.get("/example")
async def get_example():
    """Retorna un ejemplo de datos para probar la API"""
    return {
        "ejemplo": {
            "area_m2": 120.0,
            "habitaciones": 3,
            "baños": 2,
            "antiguedad": 5,
            "distancia_centro": 8.0,
            "garaje": 1,
            "jardin": 1
        },
        "descripcion": "Casa de 120m², 3 habitaciones, 2 baños, 5 años de antigüedad, a 8km del centro, con garaje y jardín"
    }

if __name__ == "__main__":
    import uvicorn
    print("Iniciando servidor API...")
    print("Documentación disponible en: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)