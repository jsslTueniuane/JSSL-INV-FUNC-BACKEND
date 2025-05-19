# **Extracción y análisis de información ONI, PARATEC y SIMEM para modelo de capacidad útil de los embalses:**

## Contenido:
1. [Introducción.](##Introducción)
2. [Estructura del proyecto.](##Estructuradelproyecto)
3. [Ejecución de proceso de transformación y analisis de datos](##TransformacionDatos)

## Introducción
Este proyecto tiene como objetivo realizar la extracción de las fuentes de información de [Climatic Prediction Center](https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php), [Parámetros técnicos del SIN (PARATEC)](https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt) y el [Sistema de Información para el Mercado de Energía Mayorista](https://www.simem.co/), realizando la integración de la información con la fuente de datos, limpieza y transformación de los datos para ser posteriormente utilizados en un modelo de Machine Learning.

## **Estructura del proyecto**

``` bash
├── Data
│   ├── ONI
│   │   └── ONI_historico.xlsx        
│   ├── PARATEC
│   │   └── PARATEC_2025-05-14.xlsx
│   ├── Results  
│   └── SIMEM
│       ├── AportesHidricos.xlsx
│       ├── ListadoEmbalses.xlsx
│       └── ReservasHidraulicasEnergía.xlsx
├── src
│   ├── Analysis
│   │   └── ExploratoryAnalysis.ipynb
│   ├── GetData
│   │   ├── ONI.py
│   │   ├── PARATEC.py
│   │   └── SIMEM.py
│   └── ResourceManager
├── test
├── .gitignore
├── function_app.py
├── host.json
├── LICENCE
├── local.settings.json
├── README.md
└── requirements.txt
```

A continuación se detalla qué contiene cada carpeta.

- ### **Data**
    En la carpeta de <code>data</code> se encuentran todos los conjuntos de datos **limpios** (es decir, únicamente con las columnas consideradas para trabajar en el modelo), todos en formato <code>.xlsx</code> y separados por carpetas según la plataforma de donde se extraen los datos.
- ### **src:**
    En la carpeta <code>src</code> se encuentra el código fuente para la extracción, estandarización, transformación y análisis de la información para disponerla para el uso del modelo. Estas tareas están repartidas en estas carpetas:
    - **Analysis:** Donde se realiza un análisis exploratorio de la información que hay en los conjuntos de datos y la clase para la obtención de los DataFrames para el entrenamiento, validación y prueba de los modelos.
    - **GetData:** Donde están las clases para la extracción de la información desde las fuentes de datos permitiendo almacenarlos en los recursos destinados.
    - **ResourceManager:** Clases para conexión a los recursos de Azure correspondientes. 
- ### **test:**
    En la carpeta <code>test</code> se encuentran las pruebas unitarias de los scripts que se encuentran en la carpeta En la carpeta <code>src</code> tiene la misma estructura y los mismos archivos solo que con el prefijo de **test**.

## Ejecución de proceso de transformación y analisis de datos:

Para ejecutar proceso de transformación y analisis de datos ejecute el Notebook de Jupyter <code>src\Analysis\ExploratoryAnalysis.ipynb</code> en orden.
