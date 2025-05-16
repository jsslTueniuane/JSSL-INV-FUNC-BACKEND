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

- <code>ONI.py</code>: Que se encarga de extraer, estandarizar y guardar la información asociada con el índice oceánico del niño (ONI) que se encuentra en [Climatic Prediction Center](https://origin.cpc.ncep.noaa.gov/products/analysis_monitoring/ensostuff/ONI_v5.php). A continuacion se detalla cada tarea:

    - **Extracción:** Se obtienen la información de un archivo <code>.txt</code> que esta en la [ruta](https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt) donde el DataFrame resultante tiene las siguientes columnas:

        | Columna | Descripción | Tipo de dato |
        |---------|-------------|--------------|
        |   Date  |  Fecha intermedia donde se calculo el valor del SST           |     Date         |
        |   SST   |  Promedio movil de tres meses consecutivos de la temperatura superficial del mar en la zona de analisis del fenomeno del niño  |       float       |
        |   ANOM  |  Indice ocenico del Niño que es el promedio de anomalías de temperatura en tres meses consecutivos   |  float            |

        La columna ***SST*** esta en el formato $M_{i}M_{i+1}M_{i+2}$ donde $M_j$ es la inicial del del mes $j$ donde se realizo el promedio del registro, con $j=i,i+1,i+2$.


    - **Estandarización:** Se crea una nueva columna en el DataFrame de ***Mes*** donde se mapea el mes $M_{i+1}$ de la secuencia $M_{i}M_{i+1}M_{i+2}$ con su correspondiente numero del mes del año (puede pensarse como $i+1 \mod 12$ ). este mapeo se realiza utlizando las siguientes asignaciones.

        ``` JSON
            {
                "DJF": 1, 
                "JFM": 2, 
                "FMA": 3, 
                "MAM": 4, 
                "AMJ": 5, 
                "MJJ": 6,
                "JJA": 7, 
                "JAS": 8, 
                "ASO": 9, 
                "SON": 10,
                "OND": 11, 
                "NDJ": 12
            }
        ```
        Posteriormente se crea la columna ***Date*** basada en las columnas ***Year*** y ***Mes** colocando como dia el primer dia del mes (1).

    - **Guardado:** Se almacenen los resultados en la ruta <code>Data\ONI\ONI_historico.xlsx</code> para luego ser utilizados en el procesos de transformación.

- <code>PARATEC.py</code>: Que se encarga de extraer, estandarizar y guardar la información asociada con los parámetros técnicos de los embalses que aportan al Sistema Interconectado Nacional (SIN) que se encuentra en [Parámetros técnicos del SIN (PARATEC)](https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt). A continuacion se detalla cada tarea:

    - **Extracción:** Se obtine la información mediante del consumo del API Rest [reportehidrologia](https://paratecbackend.xm.com.co/reportehidrologia/api/Hydrology/ReservoirInfo) donde mediante el metodo <code>GET</code> se obtiene un <code>JSON</code> la información tecnica de los embalses disponibles del SIN. 

    - **Estandarización:** Del <code>JSON</code> resultante del proceso de **Extracción** se toma la llave <code>'data'</code> y luego se transforma en un DataFame donde solamente se seleccionan las columnas ***reservoir***, ***isReservoirAggregate***, ***latitude*** y ***longitude*** donde se toman los registros que no tengas nulos en las columnas dado a que corresponden a valores agregados tanto de Colombia como de Bogota.

    - **Guardado:** Se almacenen los resultados en la ruta <code>Data\PARAREC\PARATEC_YYYY-MM-DD.xlsx</code> donde <code>YYY-MM-DD</code> corresponde a la fecha de ejecución, para luego ser utilizados en el procesos de transformación.

- <code>SIMEM.py</code>: Que se encarga de extraer, estandarizar y guardar la información asociada con el histórico de reservas hídricas de energía, el listado de embalses y los aportes hídricos en Colombia que se encuentra en el [Sistema de Información para el Mercado de Energía Mayorista](https://www.simem.co/).
    - **Listado de Embalses que sirven al Sistema Interconectado Nacional:** 

        - **Extracción:** Se utiliza el SDK <code>pydataxm</code> que pone a dispocisión el administrador del sitio y mediante la clase <code>pydatasimem.ReadSIMEM</code> colocando como parametro de <code>dataset_id='A0CF2A'</code> y colocando el rango de fechas que se quiere extraer se obtiene un DataFrame con las siguientes columnas:

            | Columna | Descripción | Tipo de dato |
            |---------|-------------|--------------|
            |   Fecha  |  Fecha de representación de la información           |    date        |
            |   CodigoEmbalse  |  Código del embalse           |    str         |
            |   NombreEmbalse   |  Nombre de los embalses del sistema interconectado nacional.  |       str       |  
            |   FechaEjecucion  |  Fecha Extracción del dato           |    date        |

        - **Estandarización:** Se retiran los registros que son iguales a  <code>'Colombia'</code> en la columna ***CodigoEmbalse*** dado a que coresponde con los agregadas para Colombia y Bogota de las variables para la fecha del registro, se seleccionan solamente las columnas ***CodigoEmbalse*** y ***NombreEmbalse*** y se eliminan los registros duplicados.  

        - **Guardado:** Se almacenen los resultados en la ruta <code>Data\SIMEM\ListadoEmbalses.xlsx</code> para luego ser utilizados en el procesos de transformación. Se obtiene un DataFrame con las siguientes columnas:

    - **Reservas Hidráulicas en Energía:** Corresponde a el "Listado que sirve como apoyo al usuario de los diferentes conjuntos de datos para extraer el nombre de los embalses que sirven al Sistema Interconectado Nacional y que se presentan en el SIMEM" ([Descripción extraida del sitio del conjunto de datos](https://www.simem.co/datadetail/B0E93334-D812-42A7-94FC-3F100BCE7038)). continuacion se detalla cada tarea para la extraccion de la información:

        - **Extracción:** Se utiliza el SDK <code>pydataxm</code> que pone a dispocisión el administrador del sitio y mediante la clase <code>pydatasimem.ReadSIMEM</code> colocando como parametro de <code>dataset_id='B0E933'</code> y colocando el rango de fechas que se quiere extraer se obtiene un DataFrame con las siguientes columnas:

        - **Estandarización:** Se retiran los registros que contienen la palabra <code>'AGREGADO'</code> en la columna ***CodigoEmbalse*** dado a que coresponde con los agregadas para Colombia y Bogota de las variables para la fecha del registro.  

        - **Guardado:** Se almacenen los resultados en la ruta <code>Data\SIMEM\ReservasHidraulicasEnergía.xlsx</code> para luego ser utilizados en el procesos de transformación. Se obtiene un DataFrame con las siguientes columnas:

    - **Aportes Hídricos en Energía:**

        - **Extracción:** Se utiliza el SDK <code>pydataxm</code> que pone a dispocisión el administrador del sitio y mediante la clase <code>pydatasimem.ReadSIMEM</code> colocando como parametro de <code>dataset_id='BA1C55'</code> y colocando el rango de fechas que se quiere extraer se obtiene un DataFrame con las siguientes columnas:

        - **Estandarización:** Se retiran los registros iguales a <code>'Colombia'</code> en la columna ***CodigoEmbalse*** dado a que coresponde con los agregados para Colombia de las variables para la fecha del registro, se seleccionan solamente las columnas ***Fecha***,***CodigoSerieHidrologica***,***RegionHidrologica***,***AportesHidricosEnergia***,***PromedioAcumuladoEnergia***, ***MediaHistoricaEnergia***.  

        - **Guardado:** Se almacenen los resultados en la ruta <code>Data\SIMEM\AportesHidricos.xlsx</code> para luego ser utilizados en el procesos de transformación. Se obtiene un DataFrame con las siguientes columnas:



### **Analysis:** 
Donde se realiza un análisis exploratorio de la información que hay en los conjuntos de datos y la clase para la obtención de los DataFrames para el entrenamiento, validación y prueba de los modelos. En esta se encuentran los siguientes archivos:

- <code>ExploratoryAnalysis.ipynb</code>: Este Notebook tiene como objetivo realizar un análisis exploratorio de la información que hay en los scripts de la carpeta <code>src/GetData</code>. Para más detalles, consulte el archivo.

- <code>TransformData.py</code>: En este script se encuentra la clase <code>JoinData</code>, la cual es la encargada de leer la información de los archivos estandarizados de las rutas <code>Data\ONI</code>, <code>Data\PARATEC</code> y <code>Data\SIMEM</code>, y unir la información (agregada por región y región hidrológica o no agregada), guardándola en la carpeta <code>Data\Results</code>. Dependiendo de si se desea la información estandarizada o no, se almacena en las carpetas <code>Data\Results\NotStandardized</code> en caso de no estar estandarizada, o en <code>Data\Results\Standardized</code> en caso de estar estandarizada.



## **ResourceManager:** 
Clases para conexión a los recursos de Azure correspondientes. **[Próximamente]**
