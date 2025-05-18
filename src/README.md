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
        |   SEAS  |  Meses en los que se realizo el promedio movil para el ONI y el SST           |     str         |
        |   YR  |  Año del mes intermedio del promedio del ONI y SST       |     int         |
        |   TOTAL   |  Promedio movil de tres meses consecutivos de la temperatura superficial del mar en la zona de analisis del fenomeno del niño  |       float       |
        |   ANOM  |  ONI   |  float            |

        La columna ***SEAS*** esta en el formato $M_{i}M_{i+1}M_{i+2}$ donde $M_j$ es la inicial del del mes $j$ donde se realizo el promedio del registro, con $j=i,i+1,i+2$.


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
        Posteriormente se crea la columna ***Date*** basada en las columnas ***Year*** y ***Mes*** colocando como dia el primer dia del mes (1).

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

            | Columna | Descripción | Tipo de dato |
            |---------|-------------|--------------|
            |   FechaPublicacion  |  Fecha de publicación del dato en el SIMEM           |    Date         |
            |   Fecha  |  Fecha de representación de la información           |    Date         |
            |   CodigoEmbalse   |  Zona geográfica en la cual se agrupan elementos con características hidrológicas similares.  |       str       |
            |   RegionHidrologica   |  Código del embalse  |       str       |
            |   VolumenUtilDiarioEnergia   |  	Volúmen Útil Diario del Embalse reportado por el agente expresado en energía  |       float       |
            |   CapacidadUtilEnergia   |  Es el máximo volumen que puede ser utilizado para la generación de energía en cada embalse. Corresponde a la diferencia entre el volumen máximo técnico y el volumen mínimo técnico.  |       float       |
            |   VolumenTotalEnergia   |  	Es el volumen máximo que puede almacenarse en un embalse, bajo condiciones normales de operación. Equivale a la suma de los siguientes volúmenes: volumen de embalse muerto, volumen mínimo técnico y volumen útil del embalse  |       float       |
            |   VertimientosEnergia   |  	Vertimientos reportados expresados en energía  |       float       |

        - **Estandarización:** Se retiran los registros que contienen la palabra <code>'AGREGADO'</code> en la columna ***CodigoEmbalse*** dado a que coresponde con los agregadas para Colombia y Bogota de las variables para la fecha del registro, se seleccionan solamente las columnas ***Fecha***, ***CodigoEmbalse***, ***RegionHidrologica***, ***VolumenUtilDiarioEnergia***, ***CapacidadUtilEnergia***, ***VolumenTotalEnergia*** y ***VertimientosEnergia***.  

        - **Guardado:** Se almacenen los resultados en la ruta <code>Data\SIMEM\ReservasHidraulicasEnergía.xlsx</code> para luego ser utilizados en el procesos de transformación. Se obtiene un DataFrame con las siguientes columnas:

    - **Aportes Hídricos en Energía:**

        - **Extracción:** Se utiliza el SDK <code>pydataxm</code> que pone a dispocisión el administrador del sitio y mediante la clase <code>pydatasimem.ReadSIMEM</code> colocando como parametro de <code>dataset_id='BA1C55'</code> y colocando el rango de fechas que se quiere extraer se obtiene un DataFrame con las siguientes columnas:

            | Columna | Descripción | Tipo de dato |
            |---------|-------------|--------------|
            |   FechaPublicacion  |  Fecha de publicación del dato en el SIMEM           |    Date         |
            |   Fecha  |  Fecha de representación de la información           |    Date         |
            |   CodigoSerieHidrologica   |  Código único para identificar una serie hidrologica o un río del Sistema Interconectado Nacional  |       str       |
            |   RegionHidrologica   |  Zona geográfica en la cual se agrupan elementos con características hidrológicas similares.  |       str       |
            |   AportesHidricosEnergia   |  	Aporte hídrico asociado con un recurso de generación despachado centralmente. |       float       |
            |   PromedioAcumuladoEnergia  |  Aportes hidricos promedio para lo que va corrido del mes.  |       float       |
            |   MediaHistoricaEnergia   |  	Promedio mensual multianual de la serie hidrológica aprobada por Acuerdo CNO  |       float       |

        - **Estandarización:** Se retiran los registros iguales a <code>'Colombia'</code> en la columna ***CodigoEmbalse*** dado a que coresponde con los agregados para Colombia de las variables para la fecha del registro, se seleccionan solamente las columnas ***Fecha***, ***CodigoSerieHidrologica***, ***RegionHidrologica***,***AportesHidricosEnergia***, ***PromedioAcumuladoEnergia*** y ***MediaHistoricaEnergia***.  

        - **Guardado:** Se almacenen los resultados en la ruta <code>Data\SIMEM\AportesHidricos.xlsx</code> para luego ser utilizados en el procesos de transformación. Se obtiene un DataFrame con las siguientes columnas:



### **Analysis:** 
Donde se realiza un análisis exploratorio de la información que hay en los conjuntos de datos y la clase para la obtención de los DataFrames para el entrenamiento, validación y prueba de los modelos. En esta se encuentran los siguientes archivos:

- <code>ExploratoryAnalysis.ipynb</code>: Este Notebook tiene como objetivo realizar un análisis exploratorio de la información que hay en los scripts de la carpeta <code>src/GetData</code>. Para más detalles, consulte el archivo.

- <code>TransformData.py</code>: En este script se encuentra la clase <code>JoinData</code>, la cual es la encargada de leer la información de los archivos estandarizados de las rutas <code>Data\ONI</code>, <code>Data\PARATEC</code> y <code>Data\SIMEM</code>, y unir la información (agregada por región y región hidrológica o no agregada), guardándola en la carpeta <code>Data\Results</code>. Dependiendo de si se desea la información estandarizada o no, se almacena en las carpetas <code>Data\Results\NotStandardized</code> en caso de no estar estandarizada, o en <code>Data\Results\Standardized</code> en caso de estar estandarizada. Antes de realizar la union de los DataSet para cada uno se realizan las siguientes transformaciones:
    - **PARATEC**: En la columna ***reservoir*** se retiranlos espacios y las letras con tildes y se reemplanzan con las letras sin tilde.
    - **ONI**: Se crean nuevos registros para que el DataSet quede con granularidad diaria (Dado a que el DataSet original tiene granularidad diaria) y se rellenan los datos nuevos con los correspondientes valores de inicio del mes para los atributos de **SST** y **ANOM**.
    - **ListadoEmbalses:** En la columna ***NombreEmbalse*** se retiranlos espacios y las letras con tildes y se reemplanzan con las letras sin tilde.  

    - **ReservasEmbalses:** Se cambia el tipo de dato de la columna **Fecha** a <code>Datetime.Date</code>. 
    - **AportesHidricos**: Se quitan todos los nulos de las columnas **PromedioAcumuladoEnergia** y **MediaHistoricaEnergia** con el registro no nulo siguiente mas cercano.

    A continuación se detalla la relación entre los DataSets:  

    ![Relación entre los DataSets](img\DiagramaEntidades.png)

    Se van a generar cuatro DataSet dos con información no agregada para las reservas de los embalses, uno estandarizado y otro no; y dos DataSets agregados por region hidrologica tambien uno estandarizado y otro no.   
    Para generar los DataSets no agregados primero se realiza la unión entre los DataSets de **PARATEC** y **ListadoEmbalses** de la siguiente manera; Primero se realizar la unión mediante las columnas ***reservior*** y ***NombreEmbalse***, luego del DataFrame resultate se realiza nuevamente la unión con el mismo DataFrame **ListadoEmbalses** pero ahora por la columna ***CodigoEmbalse***, este resultado da una DataFrame con resultan dos columnas llamadas ***CodigoEmbalse_x*** y ***CodigoEmbalse_y*** y se crea nuevamente la columna ***CodigoEmbalse*** realizan el coalesce entre esas dos columnas y luego del DataSet resultante se seleccionan unicamente las columnas ***latitude***, ***longitude*** y ***CodigoEmbalse***.

    Luego se realiza la unión de DataSet resultante ente **ListadoEmbalses** y **PARATEC**, con los Datasets **ONI** y **ReservasEmbalses** por las columnas ***Fecha*** y **Date**. De este DataFrame resultante (que llamaremos **ResultadosNoAgregados**) se selecccionan unicamente las columnas ***Fecha***, ***VolumenUtilDiarioEnergia***, ***CapacidadUtilEnergia***, ***VolumenTotalEnergia***, ***VertimientosEnergia***, ***SST***, ***ANOM***,***latitude*** y ***longitude***; se crean las columnas ***Dia***, ***Mes*** y ***Año*** basado en la columna ***Fecha*** y luego se elimina esta columna. De el DataSet **ResultadosNoAgregados** se guardan dos archivos <code>Data/Results/NotStandardized/EmbalsesNoAgregados.xlsx</code> que son los mismos datos del DataSet y <code>Data/Results/NotStandardized/EmbalsesNoAgregados.xlsx</code> que es el DataSet resultante de la estandarización de los datos mediante el metodo de <code>MinMaxScaler</code>.   

    Para generar los DataSet agregados se realiza la union de el DataSet **ReservasEmbalses**, con el **ONI** mediante las columnas ***Date*** y ***Fecha***, luego se agrupa por las columnas ***Fecha*** y ***RegionHidrologica*** con las sigientes agregaciones.
    
    - VolumenUtilDiarioEnergia - mean.
    - CapacidadUtilEnergia - mean.
    - VolumenTotalEnergia - mean.
    - VertimientosEnergia - sum.
    - SST - mean.
    - ANOM - mean.           

    Para el DataSet **AportesHidricos** se realiza la agregacion por la misma la agregación por las mismas columnas pero con las siguientes agregaciones:

    - AportesHidricosEnergia - sum.
    - PromedioAcumuladoEnergia - mean.
    - MediaHistoricaEnergia - mean.     

    De el resultado  de el Agregado de **AportesHidricos** se realiza la union con el agregado con el resultado de la union de **ONI** con **ReservasEmbalses** mediante las columnas ***Fecha*** y ***RegionHidologica*** de este resultado que llamaremos **ResultadosAgregados** se completan los datos faltantes de las columnas **MediaHistoricaEnergia** y **PromedioAcumuladoEnergia** con el datos posterior valido mas cercano. se crean las columnas ***Dia***, ***Mes*** y ***Año*** basado en la columna ***Fecha*** y se cambia la variable categorica ***RegionHidrologica*** por columnas dummys; posteriormente se elimina la columna ***Fecha***. De el DataSet **ResultadosAgregados** se guardan dos archivos <code>Data/Results/NotStandardized/EmbalsesAgregados.xlsx</code> que son los mismos datos del DataSet y <code>Data/Results/NotStandardized/EmbalsesAgregados.xlsx</code> que es el DataSet resultante de la estandarización de los datos mediante el metodo de <code>MinMaxScaler</code>.     

## **ResourceManager:** 
Clases para conexión a los recursos de Azure correspondientes. **[Próximamente]**
