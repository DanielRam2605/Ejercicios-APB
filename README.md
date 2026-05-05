# 📊 Análisis de Múltiples Conjuntos de Datos — DataInsight Analytics

**CC2005 – Algoritmos y Programación Básica**  
**Universidad del Valle de Guatemala**  
**Cristian Morales & Daniel Ramírez — Semestre I 2025**

---

## 📝 Descripción

Aplicación interactiva desarrollada con **Streamlit** que analiza cuatro conjuntos de datos de forma independiente, simulando el trabajo de una firma consultora de datos llamada *DataInsight Analytics*.

---

## 📁 Datasets utilizados

| Dataset | Archivo | Descripción |
|---|---|---|
| 🚗 Vehículos Eléctricos | `Electric_Vehicle_Population.csv` | Vehículos eléctricos registrados en distintas regiones |
| 🏋️ Gimnasio | `GymExerciseTracking.csv` | Hábitos de ejercicio y rendimiento físico de usuarios |
| 🎮 Videojuegos | `steam_store_data_2024.csv` | Popularidad y características de videojuegos en Steam 2024 |
| 🎬 Netflix | `netflix_titles.csv` | Catálogo de contenido Netflix |

---

## ⚙️ Funcionalidades

### 1. 📂 Lectura y Exploración Inicial
- Número de filas y columnas
- Nombres de columnas
- Primeras 6 filas
- Estadísticas generales de variables numéricas

### 2. ➕ Ingreso de Nuevos Datos
- Agregar nuevos registros manualmente para **Gimnasio** y **Videojuegos**

### 3. 🔍 Filtrado de Datos
Dos filtros por dataset definidos por el usuario:
- **Vehículos:** año de modelo y precio base
- **Gimnasio:** calorías quemadas y porcentaje de grasa
- **Videojuegos:** precio y porcentaje de descuento
- **Netflix:** duración de película y año de publicación

### 4. 📈 Exploración Avanzada
- Nueva variable categórica por dataset
- Conteo por categoría
- Gráfico de barras
- Análisis agrupado con métricas estadísticas

### 5. ❓ Preguntas Clave
Análisis con datos que responden preguntas de negocio para cada dataset.

### 6. 💾 Guardado de Resultados
Exporta los DataFrames actualizados como nuevos archivos CSV.

---

## 🚀 Cómo ejecutar

### 1. Instala las dependencias
```bash
pip install streamlit pandas matplotlib
```

### 2. Coloca todos los archivos CSV en la misma carpeta que `Laboratorio3.py`

### 3. Ejecuta la aplicación
```bash
streamlit run Laboratorio3.py
```

### 4. Abre tu navegador en `http://localhost:8501`

---

## 🗂️ Estructura del repositorio

```
📦 repositorio
 ┣ 📄 Laboratorio3.py
 ┣ 📄 Electric_Vehicle_Population.csv
 ┣ 📄 GymExerciseTracking.csv
 ┣ 📄 steam_store_data_2024.csv
 ┣ 📄 netflix_titles.csv
 ┗ 📄 README.md
```

---

## 🛠️ Tecnologías

- **Python 3**
- **Streamlit** — interfaz web interactiva
- **Pandas** — manipulación de datos
- **Matplotlib** — visualización de gráficos
