**Introducción**

Este proyecto analiza un conjunto de datos de **9,718 películas** provenientes de **TMDb** con el objetivo de ofrecer recomendaciones personalizadas. A partir de múltiples atributos —como calificaciones, géneros, actores principales, presupuesto, ingresos y fechas de estreno— se extraen insights que permiten sugerir películas según los gustos y el estado de ánimo del usuario.

El flujo de trabajo completo se desarrolla en el entorno de **Azure Databricks**, donde se lleva a cabo la limpieza, transformación y exploración del dataset. Para organizar y estructurar los datos de manera eficiente, el proyecto implementa la **arquitectura Medallion (Bronze, Silver y Gold)**, lo que permite un proceso ETL escalable, claro y confiable. Esta metodología establece una base sólida para generar recomendaciones más precisas y útiles.

**Dataset utilizado**

El dataset “Which movie should I watch today?” obtenido de kaggle, consta de 4 tablas en formato csv:

- **Movies.csv:** Contiene información general de cada película, sirviendo como tabla principal del dataset. Incluye campos como:
  - Id de la película, que sirve como clave primaria,
  - Título original y título publicado,
  - Fecha de estreno,
  - Puntuación promedio (vote\_average),
  - Popularidad,
  - Cantidad de votos recibidos,
  - Idioma original,
  - Géneros (como lista en formato string).
- **FilmDetails.csv:** Incluye información más detallada de las películas, enfocada en características narrativas y de producción. Entre sus atributos más relevantes se encuentran:
  - Duración (runtime),
  - Sinopsis o overview,
  - Productoras y países de producción,
  - Estado de lanzamiento (Released, Planned, etc.),
  - Restricción por edades (adult),
  - Presupuesto e ingresos.
- **MoreInfo.csv:** Aporta metadatos adicionales orientados a personalizar recomendaciones, tales como:
  - Actores principales (top cast),
  - Directores y equipos creativos,
  - Keywords o palabras clave que describen la temática,
  - Géneros adicionales,
  - Compañías asociadas.
- **PosterPath.csv:** Incluye las rutas relativas a las imágenes de póster de cada película, con atributos como:
  - Id de la película,
  - Ruta de la imagen (poster\_path).

**Entorno de desarrollo de Azure y Azure Databricks**

1. **Creación del grupo de recursos:** El nombre del grupo de recursos donde se van a aprovisionar los demás recursos de databricks es **rg-project**.

   ![Interfaz de usuario gráfica, Texto, Aplicación, Correo electrónico&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.001.png)

   ![Interfaz de usuario gráfica, Texto, Aplicación, Correo electrónico&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.002.png)

1. **Creación del entorno Azure Databricks:** El recurso **Azure Databricks**, identificado como **adbs\_fabrizzio\_quintana**, constituye el entorno de desarrollo principal del proyecto. Desde este workspace se ejecutan todos los notebooks de procesamiento, transformación y análisis de datos, aprovechando las capacidades de cómputo distribuido y la integración nativa con Azure Data Lake Storage Gen2. Este entorno permite orquestar el flujo de trabajo completo siguiendo la arquitectura medallion, garantizando eficiencia, escalabilidad y control durante cada etapa del pipeline.

   ![Interfaz de usuario gráfica, Texto, Aplicación, Correo electrónico&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.003.png)

   Como cómputo, se usa el clúster SD\_Cluster que es uno de tipo single, con el nodo de tipo Standard\_D4s\_v3 (16 GB de memoria con 4 núcleos).

   ![Captura de pantalla de computadora&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.004.png)

   Los notebooks creados están organizados en folders según su fin.

   ![Captura de pantalla con la imagen de una pantalla&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.005.png)

   Por ejemplo, la carpeta de ETL contiene los que sirven para ejecutar dicho proceso.

- **Preparación del catálogo, esquema y tablas:** Se ejecuta en **Preparacion\_Ambiente**.
- **Extract (Extracción):** Se ejecuta en:
  - **Ingest film details data**
  - **Ingest more info data**
  - **Ingest movies data**
  - **Ingest posterpath data.**
- **Transform (Transformar):** Se ejecuta en **Transform**.
- **Load (Cargar):** Se ejecuta en **Load**.

![Captura de pantalla de computadora&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.006.png)

1. **Creación del ADLS:** El recurso **ADLS** se denomina **adlsfabrizzioquintanav** y utiliza **Azure Data Lake Storage Gen2** con estructura jerárquica habilitada. Además, la región establecida es **eastus2.** 

   ![Interfaz de usuario gráfica, Texto, Aplicación, Correo electrónico&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.007.png)

La organización del almacenamiento sigue el enfoque de la **arquitectura Medallion**, donde cada contenedor corresponde a una capa específica del modelo (bronze, silver y gold).

![Interfaz de usuario gráfica, Texto, Correo electrónico&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.008.png)

En el contenedor de la capa **bronze** se cargan los cuatro archivos originales que sirven como punto de partida para el proceso de ingesta y transformación.

![Interfaz de usuario gráfica, Aplicación&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.009.png)

1. **Creación del access connector y asignarlo al ADLS:** El recurso **ac-fabrizzio** corresponde a la identidad administrada **(managed identity)** utilizada para vincular el entorno de Azure Databricks con Azure Data Lake Storage Gen2.\
   Una identidad administrada es una credencial gestionada automáticamente por Microsoft Entra ID, que permite a los recursos de Databricks autenticarse de forma segura en otros servicios de Azure sin necesidad de almacenar o gestionar contraseñas, secretos o certificados. Esto mejora significativamente la seguridad y simplifica la administración del acceso, al proporcionar un mecanismo centralizado, controlado y auditado para la autenticación entre servicios.

   Primero, se crea el access connector.

   ![Interfaz de usuario gráfica, Texto, Aplicación&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.010.png)

   Luego, se asigna al ADLS con el rol de **Storage Blob Data Contributor**.

   ![Interfaz de usuario gráfica, Texto, Aplicación, Correo electrónico&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.011.png)

   Finalmente, se crea el storage credential y los external locations por cada uno de los contenedores. El primero se llama **credential**, y los external locations se crearán al ejecutarse el notebook Preparacion\_Ambiente.

   ![Captura de pantalla de computadora&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.012.png)

1. **Creación del pipeline automatizado en Azure Data Factory:** Se creó un pipeline denominado **adffabrizzioquinta**, con el objetivo de orquestar todo el proceso ETL. Este pipeline ejecuta de manera secuencial los notebooks alojados en Azure Databricks, controlando cada etapa del flujo mediante actividades organizadas como nodos independientes. Usar esta herramienta brinda una gran ventaja por su mejor capacidad de orquestación, integración directa con otros servicios de Azure y monitoreo centralizado. Solo para este entorno, se considera un contenedor más llamado **raw** donde se van a cargar primero los archivos fuente.

   Para ello, primero se crea un linked service llamado **ls\_databricks** lo cuál sirve para conectarnos a databricks. Un linked service almacena la información necesaria para que ADF pueda autenticarse y comunicarse de forma segura con otros servicios, en este caso, permitiendo la ejecución de notebooks directamente desde Databricks.

   ![Interfaz de usuario gráfica, Texto, Aplicación&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.013.png)

   Luego, se crea el pipeline **pipeline\_ETL** donde se crean los nodos que sirven para realizar el proceso. Además, cada nodo tiene sus variables, vinculadas cada una a los widgets de los notebooks, las cuales sirven para asignar sus valores dentro de esta herramienta.

   ![Interfaz de usuario gráfica, Aplicación&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.014.png)

   Se ejecuta y se verifica que lo haya hecho con éxito.

   ![Interfaz de usuario gráfica, Aplicación&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.015.png)

   Ahora, para automatizar el proceso, se crea un nuevo ADLS denominado **adlsfabrizzioquinsource** donde se van a guardar los archivos en vez de directamente en el contenedor **raw** del anterior ADLS.

   ![Interfaz de usuario gráfica, Texto, Aplicación, Correo electrónico&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.016.png)

   Se crea el contenedor **data** donde se van a subir los archivos.

   ![Interfaz de usuario gráfica, Texto, Aplicación, Correo electrónico&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.017.png)

   Luego, en el entorno de Azure Data Factory, primero se crea el linked service **ls\_adls\_source** que va a servir para vincular el ADLS source a Data Factory.

   ![Interfaz de usuario gráfica, Texto, Aplicación, Correo electrónico&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.018.png)

   Luego, se hace lo mismo con el ADLS **adlsfabrizzioquinsource** 

   ![Interfaz de usuario gráfica, Texto, Aplicación, Correo electrónico&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.019.png)

   Ahora se van a usar datasets. Un **dataset en Azure Data Factory** representa una **vista estructurada de los datos**, es decir, una referencia a un archivo, carpeta o tabla específica dentro de un linked service. Define **qué datos** se van a usar y **dónde están ubicados**, permitiendo que las actividades del pipeline los lean o procesen.

   Primero, se crea el dataset source o fuente **ds\_source** la cual apunta al contenedor **data** que contiene todos los archivos a usar.

   ![Interfaz de usuario gráfica, Texto, Aplicación&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.020.png) 

   Luego, se crea el dataset sink o destino **ds\_sink**.

   ![Interfaz de usuario gráfica&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.021.png)

   Ahora, en el pipeline **pipeline\_carga\_datos** se crea el nodo **Copy\_ADLS\_to\_ADLS** donde se usan los datasets ya creados. Este pipeline copia los archivos contenidos en **data** de **adlsfabrizzioquinsource** a **raw** de **adlsfabrizzioquintanav.**

   ![Interfaz de usuario gráfica, Aplicación&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.022.png)

   Por último, se crean triggers (o gatilladores) que va a permitir ejecutar de manera automática el pipeline. El primer trigger que se crea es **tg\_events** en el pipeline **pipeline\_ETL** que es de tipo storage events, y que apunta al ADLS **adlsfabrizzioquintanav** en el contenedor **raw**. Este trigger se ejecuta cuando se crean nuevos archivos dentro del contenedor (o Blob) así como cuando se borran.

   ![Interfaz de usuario gráfica, Texto, Aplicación, Correo electrónico&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.023.png)

   Ahora se procede a probar la ejecución del trigger, para ello se ejecuta primero el pipeline **pipeline\_carga\_datos** de manera manual.

   ![Interfaz de usuario gráfica&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.024.png)

   Luego notamos que el trigger **tg\_events** ejecutó con éxito el pipeline **pipeline\_etl**.

   ![Interfaz de usuario gráfica, Texto, Aplicación&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.025.png)

1. **Creación del catálogo, esquemas, y tablas, y definición del modelo estrella:** En el entorno de **Azure Databricks**, una vez finalizada la ejecución del pipeline ETL, se procede a la creación del **catálogo catalog\_dev**, el cual organiza y gobierna todos los objetos de datos del proyecto. Dentro de este catálogo se definen tres esquemas que siguen la **arquitectura Medallion** (Bronze, Silver y Gold), estructurando de manera ordenada el flujo de ingesta, limpieza, transformación y consumo de los datos.

   Además, en esta etapa se establecen las **tablas necesarias para el modelo estrella**, donde la tabla de hechos y sus dimensiones quedan correctamente modeladas dentro de la capa *Gold*. Esta organización permite habilitar análisis analíticos más eficientes y consultas optimizadas, asegurando así un almacenamiento consistente, auditable y completamente gobernado bajo Unity Catalog:

   1. **Bronze:** Contiene las cuatro tablas cargadas directamente desde la capa *raw* del ADLS, sin transformaciones. Esta capa garantiza el almacenamiento fiel y seguro de los datos originales.
   1. **Silver:** En esta capa se aplican procesos de limpieza, estandarización y enriquecimiento de los datos provenientes de Bronze. Además, se realiza un análisis exploratorio que permite comprender mejor la calidad y consistencia de la información.\
      A partir de este procesamiento, se generan 3 tablas, cada una representa a una tabla del modelo estrella:
      1. **Actores\_top (Dimensión):** Representa a los actores más relevantes que han participado en cada película del catálogo. Su objetivo es desnormalizar y estructurar la información de reparto, permitiendo un análisis más preciso sobre el papel de los actores en el rendimiento, popularidad y características de las películas.
         1. id\_movies
         1. actores
      1. **Genres (Dimensión):** Diseñada para representar todos los géneros asociados a las películas presentes en el dataset. A diferencia de la información original —donde los géneros se presentan en una sola cadena separada por comas— esta dimensión normaliza y estructura dichos valores, permitiendo un análisis más detallado y relacional.
         1. id\_movies
         1. genre
      1. **Movies (Hecho):** La tabla **movies** constituye el **núcleo del modelo estrella**, al concentrar la información más relevante y cuantificable sobre cada película del dataset. Aquí se integran atributos originales del conjunto de datos y columnas derivadas mediante procesos de limpieza, enriquecimiento y estandarización.\
         Esta tabla sirve como base para análisis estadístico, generación de indicadores y recomendaciones, ya que permite medir el desempeño y características principales de cada título.
         1. id\_movies
         1. title
         1. genres
         1. language
         1. user\_score
         1. runtime\_hour
         1. runtime\_minute
         1. release\_date
         1. vote\_count
         1. classification
         1. duration\_minutes
         1. director
         1. budget\_usd
         1. revenue\_usd
         1. utility
         1. is\_profitable
         1. release\_year
         1. release\_mont	h
   1. **Golden:** Es la capa final del modelo, donde se consolidan los datos ya transformados y listos para su consumo en herramientas de análisis o plataformas de BI.\
      Aquí se generan tres tablas finales que sirven como base para dashboards y análisis avanzados, todos ellos derivados de las tablas anteriores:
      1. **golden\_actors:** Consolida información sobre los actores más relevantes dentro del conjunto de datos, permitiendo analizar su presencia en la industria y su impacto en la recepción del público. Esta tabla resume métricas clave asociadas al desempeño de los actores en las distintas producciones.
         1. actores
         1. classification
         1. release\_year
         1. cantidad
         1. avg\_user\_score
      1. **golden\_genres:** Consolida información sobre los géneros más relevantes dentro del conjunto de datos, permitiendo analizar su presencia en la industria y su impacto en la recepción del público, así como de la influencia del lenguaje en que originalmente ha sido hecho. Esta tabla resume métricas clave asociadas a la alta recepción del género en las distintas producciones.
         1. release\_year
         1. genre
         1. classification
         1. language
         1. cantidad
         1. avg\_user\_score
      1. **golden\_movies:** Integra los principales indicadores y atributos analíticos asociados a las películas presentes en el dataset. Es el resultado final del procesamiento realizado en la capa Gold, donde se consolidan métricas clave para análisis de negocio, tendencias cinematográficas, rentabilidad y comportamiento del público.
         1. title
         1. release\_year
         1. language
         1. classification
         1. is\_profitable
         1. cantidad
         1. avg\_user\_score
         1. utility
         1. avg\_duration\_minutos

![Pantalla negra con letras blancas&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.026.png)

1. **Asignación de permisos:** Se agregan un par de cuentas.

   ![Captura de pantalla de computadora&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.027.png)

   Para un mejor manejo, se crea un grupo denominado **cuentas\_agrupadas** donde se agregan a dichas cuentas.

   ![Interfaz de usuario gráfica, Aplicación&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.028.png)

   Luego, se agregan a dichas cuentas en el worksplace.

   ![Captura de pantalla de computadora&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.029.png)

   Por último, se ejecuta el notebook **seguridad\_script** donde se brindan los permisos necesarios a dicho grupo.

   ![Captura de pantalla de computadora&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.030.png)

   Se pueden revocar algunos permisos, estos están descritos en el notebook **revoke\_script**.

   ![Captura de pantalla de un celular&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.031.png)

1. **Creación de metastore:** Se crea un nuevo **metastore** que apunta al ADLS **adlsfabrizzioquintanav**, específicamente al contenedor **metastore**. El metastore es el repositorio central donde Unity Catalog almacena toda la información relacionada con catálogos, esquemas, tablas, permisos y configuraciones de gobernanza. Al configurarlo en ADLS, se garantiza que la metadata sea persistente, segura y compartida entre diferentes workspaces.\
   Además, cualquier nuevo workspace de Azure Databricks creado en la región **East US 2** se asignará automáticamente a este metastore, unificando la administración y el control de datos en un único punto.

![Pantalla de computadora con fondo negro&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.032.png)


**Entorno de producción de Azure y Azure Databricks**

1. **Creación del entorno de producción:** El servicio de Azure Databricks de producción, denominado **adbs\_fabrizzio\_prod**, se aprovisiona para poder replicar lo que se había hecho anteriormente en dicho ambiente.
1. **Despliegue en producción:** Cada vez que se realiza un pull con los cambios aplicados al archivo YAML, GitHub Actions ejecuta automáticamente el flujo definido. El pipeline corre sin errores y finaliza correctamente, indicando que la configuración y los pasos del workflow se procesaron de forma exitosa.

   ![Captura de pantalla de un celular&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.033.png)

1. **Verificación de los elementos de desarrollo en producción:**

   Se verifica que los notebooks se han subido en el entorno de producción

   ![Captura de pantalla de computadora&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.034.png)

   Además, dichos notebooks se ejecutaron de manera exitosa. Esto se demuestra al verificar que se crearon los esquemas y tablas en el ambiente de producción.

   ![Captura de pantalla de computadora&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.035.png)

   Además, se comprueba que en los contenedores también se guardaron los archivos de cada esquema exitosamente.

   ![Interfaz de usuario gráfica, Texto, Aplicación, Correo electrónico&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.036.png)


   ![Interfaz de usuario gráfica, Texto, Aplicación, Correo electrónico&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.037.png)

1. **Creación de Azure SQL Server y Database:** Con el fin de disponibilizar la información procesada en la capa *Golden*, se implementa un servidor SQL en el entorno de Azure.\
   Este servicio —Azure SQL Server junto con una base de datos SQL— permite exponer los datos finales de manera segura, estructurada y fácilmente accesible para herramientas de analítica, reporting o aplicaciones externas. La base de datos creada en este servidor recibe la información de las tablas *golden*, permitiendo su consumo por dashboards, clientes SQL, Power BI u otros sistemas de explotación de datos.

   Primero, se crea el servidor **server-fabrizzio.**

   ![Interfaz de usuario gráfica, Texto, Aplicación, Correo electrónico&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.038.png)

   Luego, se crea la base de datos **db\_fabrizzio**

   ![Interfaz de usuario gráfica, Texto, Aplicación, Correo electrónico&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.039.png)

   Luego se procede a disponibilizar la data de las tablas golden en la base de datos.

   ![Captura de pantalla de un celular&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.040.png)

   ![Captura de pantalla de computadora&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.041.png)

   Notamos que la data de dichas tablas ahora están disponible en la base de datos de SQL, lista para poder ser consumida y extraer insights.

   ![Interfaz de usuario gráfica, Texto&#x0A;&#x0A;El contenido generado por IA puede ser incorrecto.](Images/Aspose.Words.feeb53ce-6f07-4de5-b6d4-06971a022e85.042.png)