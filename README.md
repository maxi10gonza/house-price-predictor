# Predictor de Precios de Casas - Machine Learning

## Descripción del Proyecto

Este proyecto implementa un sistema completo de predicción de precios de viviendas usando Machine Learning. El sistema incluye:

- **Modelo ML**: Random Forest entrenado con 600+ registros
- **API REST**: FastAPI para servir el modelo
- **Cliente Web**: Interfaz moderna y responsive
- **Métricas**: Dashboard con información del modelo

## Caso de Estudio

**Problema**: Predicción de precios de viviendas basada en características físicas y ubicación.

**Justificación**: El mercado inmobiliario requiere herramientas para valoración automática de propiedades, útil para:
- Agentes inmobiliarios
- Compradores e inversores
- Tasadores profesionales
- Plataformas de bienes raíces

## Tecnologías Utilizadas

- **Machine Learning**: Scikit-Learn (Random Forest)
- **API**: FastAPI
- **Frontend**: HTML5, CSS3, JavaScript
- **Procesamiento**: Pandas, NumPy
- **Visualización**: Matplotlib, Seaborn

## Características del Modelo

- **Algoritmo**: Random Forest Regressor
- **Datos**: 600 registros sintéticos realistas
- **Variables**:
  - Área (m²)
  - Número de habitaciones
  - Número de baños
  - Antigüedad
  - Distancia al centro
  - Garaje (sí/no)
  - Jardín (sí/no)

## Instalación y Ejecución

### Prerrequisitos
- Python 3.8+
- pip

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd house-price-predictor
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Entrenar el modelo
```bash
cd train
python train_house_price_model.py
```
Este comando generará:
- `house_price_model.pkl`: Modelo entrenado
- `model_metrics.json`: Métricas del modelo

### 4. Iniciar la API
```bash
python api_server.py
```
La API estará disponible en: http://localhost:8000

### 5. Abrir el cliente web
Abrir `index.html` en un navegador web.

## Uso de la API

### Endpoints disponibles:

- `GET /`: Información general
- `POST /predict`: Realizar predicción
- `GET /metrics`: Métricas del modelo
- `GET /health`: Estado de la API
- `GET /example`: Ejemplo de datos

### Ejemplo de predicción:
```json
POST /predict
{
  "area_m2": 120.0,
  "habitaciones": 3,
  "baños": 2,
  "antiguedad": 5,
  "distancia_centro": 8.0,
  "garaje": 1,
  "jardin": 1
}
```

## Métricas del Modelo

- **R² Score**: ~0.95 (95% de precisión)
- **MAE**: ~$8,000 (error medio)
- **RMSE**: ~$12,000
- **Datos de entrenamiento**: 600 registros

## Interfaz Web

La interfaz incluye:
- Formulario intuitivo para características
- Predicción en tiempo real
- Visualización de métricas
- Diseño responsive
- Validación de datos

## Estructura del Proyecto

```
house-price-predictor/
├── train/
│   └── train_house_price_model.py
├── api_server.py
├── index.html
├── requirements.txt
├── README.md
├── house_price_model.pkl (generado)
├── model_metrics.json (generado)
└── feature_names.pkl (generado)
```

## Testing

### Probar la API directamente:
```bash
# Verificar estado
curl http://localhost:8000/health

# Obtener métricas
curl http://localhost:8000/metrics

# Realizar predicción
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "area_m2": 150,
       "habitaciones": 4,
       "baños": 3,
       "antiguedad": 10,
       "distancia_centro": 5,
       "garaje": 1,
       "jardin": 1
     }'
```










"# house-price-predictor" 
