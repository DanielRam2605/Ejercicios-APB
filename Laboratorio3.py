import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("Análisis de datos Cristian Morales y Daniel Ramirez")
categorias = ["Vehículos eléctricos", "Gimnasio", "Videojuegos", "Netflix"]
tipo_csv = st.sidebar.selectbox("Dataset",categorias)
if tipo_csv == "Vehículos eléctricos":
    df = pd.read_csv("Electric_Vehicle_Population.csv")
elif tipo_csv == "Gimnasio":
    df = pd.read_csv("GymExerciseTracking.csv")
elif tipo_csv == "Videojuegos":
    df = pd.read_csv("steam_store_data_2024.csv")
else:
    df = pd.read_csv("netflix_titles.csv")
if tipo_csv not in st.session_state:
    st.session_state[tipo_csv] = df
#Lo hice para no tener que poner st.session_state[tipo_csv]
df = st.session_state[tipo_csv]
st.subheader("Exploración")

st.write("Filas:", df.shape[0])
st.write("Columnas:", df.shape[1])
st.write("Nombres de columnas:", df.columns)
st.write("Primeras 6 filas:")
st.dataframe(df.head(6))
st.write("Estadísticas:")
st.write(df.describe())

if tipo_csv == "Videojuegos":
    if "videojuegos" not in st.session_state:
        st.session_state.videojuegos = df
    if "boton_agregar" not in st.session_state:
        st.session_state.boton_agregar = False
    reviews = ["Very/Overwhelmingly Negative", "Mostly Negative", "Mixed", "Mostly Positive", "Very Positive", "Overwhelmingly Positive"]
    if st.button("Agregar nuevo videojuego"):
        st.session_state.boton_agregar = True
    if st.session_state.boton_agregar == True:
        #Se lo pongo en inglés para que no se vea tan diferente
        titulo = st.text_input("¿Cuál es el título del juego?")
        descripcion = st.text_input(f"Ingresa una descripción sobre {titulo}")
        precio = st.number_input(f"Ingresa el precio de {titulo}", min_value=0.0, format="%.2f")
        #Lo volví un str para que encaje con los otros datos
        porcentaje_ventas = st.text_input(f"Ingresa el descuento de {titulo} (número%)")
        reviews_recientes = st.selectbox(f"Selecciona el tipo de reseña reciente de {titulo}", reviews)
        review_general = st.selectbox(f"Selecciona el tipo de reseña general de {titulo}", reviews)
        if st.button("Confirmar videojuego"):
            nuevo_videojuego = pd.DataFrame([[titulo,descripcion,precio,porcentaje_ventas,reviews_recientes,review_general]], columns=["title","description","price","salePercentage","recentReviews","allReviews"])
            st.session_state.videojuegos = pd.concat([st.session_state.videojuegos, nuevo_videojuego], ignore_index=True)
            st.success("¡Videojuego agregado!")
            st.session_state.boton_agregar = False
            st.dataframe(st.session_state.videojuegos)
   
   
    st.subheader("Filtros")
    st.write("Precio")
    df["price"] = pd.to_numeric(df["price"].astype(str).str.replace(r"\$", "", regex=True),errors="coerce") #Esto hace que pasen de ser $x a solo x, para poder ordenar los datos, de lo contrario no se puede.
    precio = st.number_input("Videojuegos con precio menor a", min_value=0.0)
    filtro1 = df[df["price"] > precio]
    st.dataframe(filtro1)
    st.write("Descuento")
    df["salePercentage"] = pd.to_numeric(df["salePercentage"].astype(str).str.replace("%", ""),errors="coerce")
    descuento = st.number_input("Videojuegos con descuento menor a (%)", min_value=0.0, max_value=100.0)
    filtro2 = df[df["salePercentage"].abs() < descuento] #El problema es que los porcentajes están negativos
    st.dataframe(filtro2)

# Lo que hace .apply es ejecutar un tipo de ciclo for que hace un repaso de cada línea de la columna requerida
    st.subheader("Nueva variable categórica")
    def GamaJuego(precio_videojuego):
        if precio_videojuego < 10:
            return "Gama Baja"
        elif precio_videojuego <= 24:
            return "Gama Media"
        else:
            return "Gama Alta"
    df["GamaJuego"] = df["price"].apply(GamaJuego)
    st.dataframe(df[["price", "GamaJuego"]])
    

#Honestamente, no sabía que significaba el conteo por categoría, así que le preguntá a Chat y esto me apareció. 
    st.subheader("Conteo por categoría")
    conteo = df["GamaJuego"].value_counts()
    st.write(conteo)


    st.subheader("Juegos por categoría")
    resumen = df.groupby("GamaJuego")["price"].count()
    fig, ax = plt.subplots()
    resumen.plot(kind='bar', ax=ax)
    ax.set_ylabel("Cantidad de videojuegos")
    ax.set_xlabel("Tipo de gama")
    ax.set_title("Cantidad de videojuegos por gama")
    st.pyplot(fig)

    st.subheader("Análisis agrupado")
    promedio_precio = df.groupby("GamaJuego")["price"].mean()
    desviacion_precio = df.groupby("GamaJuego")["price"].std()
    promedio_descuento = df.groupby("GamaJuego")["salePercentage"].mean()
    st.write("Promedio del precio de venta", promedio_precio)
    st.write("Desviación estándar del precio", desviacion_precio)
    st.write("Promedio del descuento de venta", promedio_descuento.abs())   #.abs para que quede positivo

    if st.button("Guardar CSV actualizado"):
        df.to_csv("steam_store_data_2024_Actualizado.csv", index=False)
elif tipo_csv == "Gimnasio":
    if "gimnasio" not in st.session_state:
        st.session_state.gimnasio = df
    if "boton" not in st.session_state:
        st.session_state.boton = False
    generos = ["Male", "Female"]
    ejercicios = ["Yoga", "HIIT", "Cardio", "Strength"]
    if st.button("Agregar nuevo perfil"):
        st.session_state.boton = True
    if st.session_state.boton == True:
        edad = st.number_input("Ingresa la edad del cliente", min_value= 18, max_value=100)
        genero = st.selectbox("Ingresa el género del cliente", generos)
        peso = st.number_input("Ingresa el peso en KG del cliente", min_value=0.0, format="%.2f")
        altura = st.number_input("Ingresa la altura del cliente en metros", min_value= 0.5, format="%.2f")
        BPMax = st.number_input("Ingresa el máximo BPM", min_value=0)
        BPM_promedio = st.number_input("Ingresa el promedio de BPM", min_value=0)
        BPM_descanso = st.number_input("Ingresa los BPM al descansar", min_value=0)
        duracion_sesiones = st.number_input("Ingresa la duración de las sesiones", min_value=0.0, format="%.2f")
        calorias = st.number_input("Ingresa las calorías quemadas del usuario", min_value=0)
        tipo_ejercicio = st.selectbox("Indica el tipo de ejercicio", ejercicios)
        porcentaje_grasa = st.number_input("Ingresa el porcentaje de grasa", min_value=0.0, format="%.2f")
        agua = st.number_input("Ingresa los litros de agua tomados por el usuario", min_value=0.0, format="%.2f")
        frecuencia = st.number_input("Ingresa la frecuencia de asistencia al gimnasio del usuario", min_value=0, max_value=7)
        nivel = st.selectbox("Indica el nivel de experiencia del usuario", [1,2,3])
        BMI = st.number_input("Ingresa el BMI", min_value=0.0, format="%.2f")
        if st.button("Confirmar datos"):
            nuevo_usuario = pd.DataFrame([[edad, genero, peso, altura, BPMax, BPM_promedio, BPM_descanso, duracion_sesiones, calorias, tipo_ejercicio, porcentaje_grasa, agua, frecuencia, nivel, BMI]], columns=["Age", "Gender", "Weight (kg)", "Height (m)", "Max_BPM", "Avg_BPM", "Resting_BPM", "Session_Duration (hours)", "Calories_Burned", "Workout_Type", "Fat_Percentage", "Water_Intake (liters)", "Workout_Frequency (days/week)", "Experience_Level", "BMI"])
            st.session_state.gimnasio = pd.concat([st.session_state.gimnasio, nuevo_usuario], ignore_index=True)
            st.success("¡Usuario agregado!")
            st.session_state.boton = False
            st.dataframe(st.session_state.gimnasio)
   
   
    st.subheader("Filtros")
    st.write("Filtro de calorías quemadas")
    calorias_quemadas = st.number_input("Usuarios con más o igual calorías quemadas que", min_value=0)
    filtro1 = df[df["Calories_Burned"] >= calorias_quemadas]
    st.dataframe(filtro1)
    st.write("Porcentaje de grasa")
    grasa = st.number_input("Usuarios con menor o igual porcentaje de grasa que",min_value= 0)
    filtro2 = df[df["Fat_Percentage"] <= grasa]
    st.dataframe(filtro2)


    st.subheader("Nueva variable categórica")
    def frecuencia_asistencia(asistencia):
        if asistencia < 3:
            return "Baja"
        elif asistencia <= 5:
            return "Moderada"
        else:
            return "Alta"
    df["NivelFrecuencia"] = df["Workout_Frequency (days/week)"].apply(frecuencia_asistencia)
    st.dataframe(df[["Workout_Frequency (days/week)", "NivelFrecuencia"]])


    st.subheader("Conteo por categoría")
    conteo = df["NivelFrecuencia"].value_counts()
    st.write(conteo)


    st.subheader("Usuarios por frecuencia de asistencia al gimnasio")
    resumen = df.groupby("NivelFrecuencia")["Workout_Frequency (days/week)"].count()
    fig, ax = plt.subplots()
    resumen.plot(kind='bar', ax=ax)
    ax.set_ylabel("Usuarios")
    ax.set_xlabel("Tipo de frecuencia")
    ax.set_title("Usuarios por nivel de frecuencia")
    st.pyplot(fig)

    st.subheader("Análisis agrupado")
    promedio_duracion = df.groupby("NivelFrecuencia")["Session_Duration (hours)"].mean()
    promedio_experiencia = df.groupby("NivelFrecuencia")["Experience_Level"].mean()
    desviacion_bmi = df.groupby("NivelFrecuencia")["BMI"].std()
    st.write("Promedio de horas de entreno", promedio_duracion)
    st.write("Promedio del nivel de experiencia de los usuarios", promedio_experiencia)
    st.write("Desviación estándar de BMI", desviacion_bmi)

    if st.button("Guardar CSV actualizado"):
        df.to_csv("GymExerciseTracking_Actualizado.csv", index=False)
elif tipo_csv == "Vehículos eléctricos":
    st.subheader("Filtros")
    st.write("Modelo del carro")
    modelo = st.number_input("Modelos de carros más antiguos que", min_value= 2000, max_value= 2025)
    filtro1 = df[df["Model Year"] < modelo]
    st.dataframe(filtro1)
    st.write("Precio base")
    precio_base = st.number_input("Modelos de carros con precio base menor a", min_value= 0, max_value=845000)
    filtro2 = df[df["Base_MSRP"] < precio_base]
    st.dataframe(filtro2)


    st.subheader("Nueva variable categórica")
    def RangoCategoria(RangoElectrico):
        if RangoElectrico < 100:
            return "Bajo"
        elif RangoElectrico <= 250:
            return "Medio"
        else:
            return "Alto"
    df["RangoCategoria"] = df["Electric_Range"].apply(RangoCategoria)
    st.dataframe(df[["Electric_Range", "RangoCategoria"]])


    st.subheader("Conteo por categoría")
    conteo = df["RangoCategoria"].value_counts()
    st.write(conteo)

    st.subheader("Vehículos por rango eléctrico")
    resumen = df.groupby("RangoCategoria")["Electric_Range"].count()
    fig, ax = plt.subplots()
    resumen.plot(kind='bar', ax=ax)
    ax.set_ylabel("Vehículos")
    ax.set_xlabel("Rango Eléctrico")
    ax.set_title("Vehículos por rango eléctrico")
    st.pyplot(fig)

    st.subheader("Análisis agrupado")
    promedio_precio_base = df.groupby("RangoCategoria")["Base_MSRP"].mean()
    promedio_modelo = df.groupby("RangoCategoria")["Model Year"].mean()
    desviacion_rango = df.groupby("RangoCategoria")["Electric_Range"].std()
    st.write("Promedio de precio base", promedio_precio_base)
    st.write("Promedio del año de modelos", promedio_modelo)
    st.write("Desviación estándar del rango eléctrico", desviacion_rango)

    if st.button("Guardar CSV actualizado"):
        df.to_csv("Electric_Vehicle_Population_Actualizado.csv", index=False)
elif tipo_csv == "Netflix":
    st.subheader("Filtros")
    df = df[df["type"] == "Movie"].copy() #Hace una copia de la columna para trabajar solo con películas
    df["duration_int"] = df["duration"].str.extract(r"(\d+)").astype(float) #Quita min y ya lo deja como float
    df["year_added"] = pd.to_datetime(df["date_added"], errors="coerce").dt.year
    st.write("Duración de pelçula")
    duracion = st.number_input("Películas con una duración mayor a", min_value= 0)
    filtro1 = df[df["duration_int"] > duracion]
    st.dataframe(filtro1)
    st.write("Años")
    fecha_publicacion = st.number_input("Películas más antiguas que", min_value=1900, max_value=2025)
    filtro2 = df[df["year_added"] < fecha_publicacion]
    st.dataframe(filtro2)


    st.subheader("Nueva variable categórica")
    def tipo_audiencia(audiencia):
        if audiencia in ["G", "TV-Y", "TV-G", "TV-Y7", "TV-Y7-FV"]:
            return "Niños"
        elif audiencia in ["PG", "TV-PG"]:
            return "Adolescentes"
        elif audiencia in ["PG-13", "TV-14"]:
            return "Adultos Jóvenes"
        else:
            return "Adultos"
    df["TipoAudiencia"] = df["rating"].apply(tipo_audiencia)
    st.dataframe(df[["rating", "TipoAudiencia"]])


    st.subheader("Conteo por categoría")
    conteo = df["TipoAudiencia"].value_counts()
    st.write(conteo)

    st.subheader("Contenido por audiencia")
    resumen = df.groupby("TipoAudiencia")["rating"].count()
    fig, ax = plt.subplots()
    resumen.plot(kind='bar', ax=ax)
    ax.set_ylabel("Usuarios")
    ax.set_xlabel("Tipo de adudiencia")
    ax.set_title("Contenido por tipo de audiencia")
    st.pyplot(fig)

    st.subheader("Análisis agrupado")
    def tipo_contenido(grupo):
        return grupo["type"].mode()[0]
    tipo_comun = df.groupby("TipoAudiencia").apply(tipo_contenido)
    st.write("Tipo de contenido más común:")
    st.dataframe(tipo_comun)
    promedio_duracion = df.groupby("TipoAudiencia")["duration_int"].mean()
    st.write("Promedio de duración", promedio_duracion)
    if st.button("Guardar CSV actualizado"):
        df.to_csv("netflix_titles_Actualizado.csv", index=False)