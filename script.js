const API_BASE = 'http://localhost:8000';
        
        // Cargar métricas del modelo al cargar la página
        async function loadModelMetrics() {
            try {
                const response = await fetch(`${API_BASE}/metrics`);
                const metrics = await response.json();
                
                const metricsHtml = `
                    <div style="margin-bottom: 20px;">
                        <h3>🎯 Precisión del Modelo</h3>
                        <p><strong>R² Score:</strong> ${(metrics.r2_test * 100).toFixed(2)}%</p>
                        <p><strong>Error Medio:</strong> $${metrics.mae_test.toLocaleString()}</p>
                        <p><strong>Datos de entrenamiento:</strong> ${metrics.n_samples} casos</p>
                    </div>
                    <div>
                        <h4>📋 Características del modelo:</h4>
                        <ul style="margin-top: 10px;">
                            ${metrics.features.map(feature => `<li>${feature}</li>`).join('')}
                        </ul>
                    </div>
                `;
                
                document.getElementById('modelMetrics').innerHTML = metricsHtml;
                
                // Mostrar métricas en tarjetas
                const metricsGrid = document.getElementById('metricsGrid');
                metricsGrid.innerHTML = `
                    <div class="metric-card">
                        <div class="metric-value">${(metrics.r2_test * 100).toFixed(1)}%</div>
                        <div class="metric-label">Precisión (R²)</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">$${Math.round(metrics.mae_test).toLocaleString()}</div>
                        <div class="metric-label">Error Medio</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">${metrics.n_samples}</div>
                        <div class="metric-label">Datos de Entrenamiento</div>
                    </div>
                `;
                metricsGrid.style.display = 'grid';
                
            } catch (error) {
                document.getElementById('modelMetrics').innerHTML = 
                    '<p style="color: red;">Error al cargar métricas del modelo</p>';
            }
        }

        // Manejar envío del formulario
        document.getElementById('predictionForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());
            
            // Convertir valores numéricos
            data.area_m2 = parseFloat(data.area_m2);
            data.habitaciones = parseInt(data.habitaciones);
            data.baños = parseInt(data.baños);
            data.antiguedad = parseInt(data.antiguedad);
            data.distancia_centro = parseFloat(data.distancia_centro);
            data.garaje = parseInt(data.garaje);
            data.jardin = parseInt(data.jardin);
            
            // Mostrar loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('predictBtn').disabled = true;
            document.getElementById('result').innerHTML = '';
            
            try {
                const response = await fetch(`${API_BASE}/predict`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    document.getElementById('result').innerHTML = `
                        <div class="result success">
                            <h3>Predicción Exitosa</h3>
                            <div class="price">USD ${result.precio_formateado}</div>
                            <p>Precio estimado para la propiedad</p>
                        </div>
                    `;
                } else {
                    throw new Error(result.detail || 'Error en la predicción');
                }
                
            } catch (error) {
                document.getElementById('result').innerHTML = `
                    <div class="result error">
                        <h3>Error</h3>
                        <p>${error.message}</p>
                    </div>
                `;
            } finally {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('predictBtn').disabled = false;
            }
        });

        // Cargar métricas al cargar la página
        loadModelMetrics();