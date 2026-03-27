# Presentación: Clasificador de Reclamos

## Slide 1: Planteamiento del problema
**Visual:** Título grande "Clasificador Automático de Reclamos" con iconos de atención al cliente y enrutamiento inteligente.

**Contenido:**
- **Contexto:** Actualmente, las empresas reciben un volumen masivo de quejas y reclamos de clientes. El proceso de leer, analizar y derivar cada caso manualmente al departamento correcto es un cuello de botella que retrasa las soluciones y genera insatisfacción en el cliente.
- **El Problema a resolver:** Categorizar / Clasificar tickets o reclamos de forma manual genera altos tiempos de respuesta y está propenso a errores humanos.
- **Escenario Práctico:** Imaginemos una empresa que recibe miles de reclamos. Tienen una alta incidencia en casos críticos como "Entrega del producto o servicio" y "Cobros indebidos". Un sistema de clasificación automática permite que, en el momento en que un cliente simplemente redacta de manera libre la descripción de su queja, el sistema comprenda el texto mediante Procesamiento de Lenguaje Natural y automáticamente etiquete el ticket con la categoría correcta, permitiendo alertar al equipo de soporte o logística en milisegundos.

## Slide 2: Uso de Machine Learning
**Visual:** Diagrama simple mostrando texto libre entrando a una caja de Machine Learning (TF-IDF + XGBoost) y saliendo con una etiqueta de clasificación entre 8 macro-categorías.

**Contenido:**
- **Enfoque Tecnológico:** Machine Learning con Procesamiento de Lenguaje Natural (NLP).
- **Modelo utilizado:** Pipeline Híbrido (**TF-IDF + XGBoost Classifier**). El sistema utiliza TF-IDF (Term Frequency - Inverse Document Frequency) con bigramas (`ngram_range=(1,2)`) y hasta 5,000 features para extraer el significado y la importancia de las palabras escritas libremente por el usuario, e introduce esos vectores a un algoritmo de árboles de decisión potenciado por gradiente (XGBoost) para clasificar a alta velocidad.
- **Tipo de aprendizaje:**
  - **Supervisado:** El modelo fue entrenado usando más de 60,000 textos/quejas reales donde ya se conocía previamente el motivo exacto de la reclamación.
  - **Multicategoría:** El algoritmo clasifica y envía el reclamo hacia la más probable entre **8 Macro-Categorías** definidas por agrupación semántica: *Entrega del producto o servicio, Cobros indebidos, Garantías y reparaciones, Cambios y devoluciones, Depósitos y reembolsos, Contratos, Información y publicidad, y Otros*.

## Slide 3: Datos y preparación (ETL)
**Visual:** Flujo de datos: Excel (81k filas) -> Limpieza selectiva -> Dataset enriquecido (~60.6k filas) -> Agrupación en 8 macro-categorías -> Texto sintético -> CSV final.

**Contenido:**
- **Dataset de Origen:** Archivo original de quejas de PROFECO (`Quejas.xlsx`) conteniendo 81,883 registros con 18 variables distintas (Sector, costos, tipo de problema, medio de ingreso, modalidad de compra, etc.).
- **Proceso de Limpieza (Data Cleaning):**
  - **Estrategia inteligente de limpieza selectiva:** En lugar de eliminar toda fila con algún nulo (`dropna()` global que dejaba ~27,400 filas), se eliminaron **únicamente** las filas sin valor en la variable target (`MOTIVO_RECLAMACION`) o en `TIPO_RECLAMACION`, conservando **~60,600 filas** — más del **doble** del enfoque anterior.
  - **Imputación de nulos:** Los valores nulos en columnas categóricas (Sector, Procedimiento, Modalidad de Compra, etc.) se imputaron con el valor "Desconocido" en lugar de descartarlos, maximizando la retención de datos.
  - **Normalización:** Se reemplazaron guiones `-` por `NaN` real para estandarizar el tratamiento de valores faltantes.
- **Ingeniería de Características (Feature Engineering):**
  - **Agrupación del target en macro-categorías:** El target original (`MOTIVO_RECLAMACION`) contenía ~137 categorías granulares, muchas con menos de 10 registros. Se diseñó un mapeo experto de ~120 motivos originales hacia **8 macro-categorías** por afinidad temática, permitiendo al modelo generalizar eficientemente.
  - **Construcción de texto sintético:** Se concatenaron las columnas categóricas descriptivas (`TIPO_RECLAMACION`, `SECTOR`, `BIEN O SERV`, `TIPO PROD`, `MODALIDAD COMPRA`, `MODALIDAD PAGO`, `MEDIO INGRESO`, `PROCEDIMIENTO`, `PROB ESPECIAL`) en un solo campo `texto` normalizado a minúsculas, creando una representación textual rica para el modelo TF-IDF.
  - **Dataset exportado:** El dataset resultante contiene solo 2 columnas (`texto`, `CATEGORIA`) exportadas a `quejas_limpias.csv`.

## Slide 4: Proceso de Entrenamiento y Evaluación
**Visual:** Diagrama de partición de datos (80% Entrenamiento / 20% Prueba), pipeline TF-IDF → XGBoost, y gráficos de métricas (Accuracy ~79%, F1 ponderado ~80%).

**Contenido:**
- **Partición de Datos (Split):** El dataset limpio se dividió estratégicamente en **80% para entrenamiento** y **20% para pruebas** (`test_size=0.2`). Se usó una partición *estratificada* para garantizar que todas las categorías, incluso las de menor frecuencia, estuvieran representadas proporcionalmente en ambas etapas.
- **Vectorización TF-IDF:**
  - Bigramas (`ngram_range=(1,2)`) para capturar contexto entre palabras.
  - Máximo de 5,000 features (`max_features=5000`) y frecuencia mínima de 2 documentos (`min_df=2`).
  - TF sublineal (`sublinear_tf=True`) para normalizar el efecto de términos muy frecuentes.
- **Aspectos Técnicos del Entrenamiento:**
  - **Balanceo de Clases:** Para evitar que el modelo ignorara los reclamos menos comunes, se calcularon e inyectaron *pesos de muestra balanceados* en el aprendizaje (`compute_sample_weight`), penalizando más los errores en clases minoritarias.
  - **Modelo Base:** Se entrenó un XGBoost con parámetros conservadores (300 estimadores, profundidad 6, learning rate 0.1) como línea base.
  - **Optimización de Hiperparámetros:** Se aplicó `RandomizedSearchCV` con **20 iteraciones** y **Validación Cruzada 3-fold**, optimizando F1-Score ponderado. Se exploró un espacio de 9 hiperparámetros distintos (n_estimators, max_depth, learning_rate, subsample, colsample_bytree, min_child_weight, gamma, reg_alpha, reg_lambda).
  - **Mejores Hiperparámetros encontrados:** `n_estimators=500`, `max_depth=5`, `learning_rate=0.05`, `subsample=0.7`, `colsample_bytree=0.8`, `min_child_weight=3`, `gamma=0.1`, `reg_lambda=1.0`, `reg_alpha=0`.
  - **Validación Cruzada 5-fold del mejor modelo:** F1 ponderado = **82.19% ± 0.48%**, demostrando alta estabilidad y consistencia.
- **Resultados obtenidos en el Conjunto de Prueba (20% — 12,126 registros):**
  - **Exactitud (Accuracy):** **~79%**
  - **F1-Score (Ponderado):** **~80%**
- **Rendimiento destacado por categoría:**
  - "Cobros indebidos": **92% F1-Score** (precision 93%, recall 91%)
  - "Garantías y reparaciones": **92% F1-Score** (precision 92%, recall 92%)
  - "Contratos": **89% F1-Score** (precision 91%, recall 88%)
  - "Entrega del producto o servicio": **87% F1-Score** (precision 90%, recall 83%)
  - "Información y publicidad": **66% F1-Score** (recall 85% — identifica la mayoría de los casos)
- **Mejora significativa:** El rediseño del ETL (mayor retención de datos con limpieza inteligente + agrupación en macro-categorías) elevó las métricas de ~56% Accuracy / ~58% F1 a **~79% Accuracy / ~80% F1**, una mejora de más de **20 puntos porcentuales**.

## Slide 5: Implementación y Demo
**Visual:** Arquitectura Cliente-Servidor. Frontend premium (HTML/CSS/JS) → petición JSON → FastAPI Backend → modelo TF-IDF + XGBoost (.pkl) → predicción con probabilidades.

**Contenido:**
- **Arquitectura Backend:** El clasificador ya no es solo un experimento en un *Notebook*; está implementado como una API robusta utilizando **FastAPI** (Python). El backend está modularizado con un archivo de configuración centralizado (`config.py`) que gestiona rutas del modelo, métricas y datos.
- **Motor de Inferencia:** Al levantar el servidor, el modelo entrenado junto con sus artefactos (modelo XGBoost, vectorizador TF-IDF, codificador de etiquetas y lista de categorías) se cargan en memoria desde `model.pkl` para responder instantáneamente.
- **Frontend Profesional:** Interfaz web construida con HTML5/CSS3/JavaScript Vanilla, con diseño premium que incluye:
  - Tipografías profesionales (DM Serif Display, Source Sans 3, JetBrains Mono).
  - Efectos visuales modernos: glassmorphism, gradientes suaves, micro-animaciones.
  - Indicador de estado de la API en tiempo real (conectada/desconectada).
  - Barra de confianza animada y ranking Top 5 de categorías.
- **La Demo en Acción:**
  1. **Input:** En la interfaz, el cliente simplemente introduce el problema o reclamo escribiéndolo en lenguaje natural en un cuadro de texto (Ej. *"Compré una lavadora y tiene defectos de fábrica..."*).
  2. **Proceso:** El endpoint `POST /api/predict` de FastAPI recibe el texto de descripción en formato JSON (`{ "texto": "..." }`), aplica el procesamiento de lenguaje computacional (TF-IDF) y lo envía a través del modelo entrenado.
  3. **Output:** Dinámicamente, la interfaz muestra la categoría detectada del reclamo junto a un medidor del **porcentaje de confianza** con animación, listando adicionalmente las **5 mejores probabilidades** alternas para dar un contexto extenso al asesor de servicio.
- **Endpoints de la API:**
  - `POST /api/predict` — Clasificación de texto en tiempo real.
  - `GET /api/categories` — Lista de las 8 macro-categorías del modelo.
  - `GET /api/metrics` — Métricas de evaluación del modelo (classification report, matriz de confusión, mejores hiperparámetros).
  - `GET /api/stats` — Estadísticas del dataset (total registros, distribución por categoría).
  - `GET /api/health` — Health check del servidor y estado del modelo.
- **Escalabilidad:** Los endpoints de métricas y estadísticas permiten que un Dashboard pueda monitorear el rendimiento del modelo en tiempo real a futuro.
