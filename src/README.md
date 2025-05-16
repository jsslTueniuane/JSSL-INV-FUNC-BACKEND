# Extracción, estandarización, transformación y análisis de la información.

## Introducción:

En la carpeta <code>src</code> se encuentra el código fuente para la extracción, estandarización, transformación y análisis de la información para disponerla para el uso del modelo. Estas tareas están repartidas en estas carpetas:

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
├── src <---(Here)
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
Donde:

### **GetData:** 
Donde están las clases para la extracción de la información desde las fuentes de datos permitiendo almacenarlos en los recursos destinados. En esta carpeta se encuentran los siguientes archivos:

- <code>ONI.py</code>: Que se encarga de extraer, estandarizar y guardar la información asociada con el índice oceánico del niño (ONI) que se encuentra en [Climatic Prediction Center](https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php).

- <code>PARATEC.py</code>: Que se encarga de extraer, estandarizar y guardar la información asociada con los parámetros técnicos de los embalses que aportan al Sistema Interconectado Nacional (SIN) que se encuentra en [Parámetros técnicos del SIN (PARATEC)](https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt).

- <code>SIMEM.py</code>: Que se encarga de extraer, estandarizar y guardar la información asociada con el histórico de reservas hídricas de energía, el listado de embalses y los aportes hídricos en Colombia que se encuentra en el [Sistema de Información para el Mercado de Energía Mayorista](https://www.simem.co/).

### **Analysis:** 
Donde se realiza un análisis exploratorio de la información que hay en los conjuntos de datos y la clase para la obtención de los DataFrames para el entrenamiento, validación y prueba de los modelos. En esta se encuentran los siguientes archivos:

- <code>ExploratoryAnalysis.ipynb</code>: Este Notebook tiene como objetivo realizar un análisis exploratorio de la información que hay en los scripts de la carpeta <code>src/GetData</code>. Para más detalles, consulte el archivo.

- <code>TransformData.py</code>: En este script se encuentra la clase <code>JoinData</code>, la cual es la encargada de leer la información de los archivos estandarizados de las rutas <code>Data\ONI</code>, <code>Data\PARATEC</code> y <code>Data\SIMEM</code>, y unir la información (agregada por región y región hidrológica o no agregada), guardándola en la carpeta <code>Data\Results</code>. Dependiendo de si se desea la información estandarizada o no, se almacena en las carpetas <code>Data\Results\NotStandardized</code> en caso de no estar estandarizada, o en <code>Data\Results\Standardized</code> en caso de estar estandarizada.



## **ResourceManager:** 
Clases para conexión a los recursos de Azure correspondientes. **[Próximamente]**
