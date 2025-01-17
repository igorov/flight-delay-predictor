# Desafío para Ingeniero de Software (ML & LLMs)

## Descripción general

Bienvenido al Desafío de Aplicación para **Ingeniero de Software (ML & LLMs)**. En este reto, tendrás la oportunidad de acercarte a una parte de la realidad del rol y demostrar tus habilidades y conocimientos en machine learning y la nube.

## Problema

Se te ha proporcionado un notebook de Jupyter (`exploration.ipynb`) con el trabajo de un Científico de Datos (en adelante, el DS). El DS entrenó un modelo para predecir la probabilidad de **retraso** de un vuelo que despega o aterriza en el aeropuerto SCL. El modelo fue entrenado con datos públicos y reales. A continuación, se describe el conjunto de datos:

|Columna|Descripción|
|-----|-----------|
|`Fecha-I`|Fecha y hora programada del vuelo.|
|`Vlo-I`|Número de vuelo programado.|
|`Ori-I`|Código de ciudad de origen programada.|
|`Des-I`|Código de ciudad de destino programada.|
|`Emp-I`|Código de aerolínea programada.|
|`Fecha-O`|Fecha y hora de operación del vuelo.|
|`Vlo-O`|Número de vuelo operado.|
|`Ori-O`|Código de ciudad de origen operada.|
|`Des-O`|Código de ciudad de destino operada.|
|`Emp-O`|Código de aerolínea operada.|
|`DIA`|Día del mes de operación del vuelo.|
|`MES`|Número del mes de operación del vuelo.|
|`AÑO`|Año de operación del vuelo.|
|`DIANOM`|Día de la semana de operación del vuelo.|
|`TIPOVUELO`|Tipo de vuelo, I = Internacional, N = Nacional.|
|`OPERA`|Nombre de la aerolínea que opera el vuelo.|
|`SIGLAORI`|Nombre de la ciudad de origen.|
|`SIGLADES`|Nombre de la ciudad de destino.|

Además, el DS consideró relevante la creación de las siguientes columnas:

|Columna|Descripción|
|-----|-----------|
|`high_season`|1 si `Fecha-I` está entre el 15-Dic y el 3-Mar, o el 15-Jul y el 31-Jul, o el 11-Sep y el 30-Sep, 0 en caso contrario.|
|`min_diff`|Diferencia en minutos entre `Fecha-O` y `Fecha-I`.|
|`period_day`|Mañana (entre las 5:00 y las 11:59), tarde (entre las 12:00 y las 18:59) y noche (entre las 19:00 y las 4:59), basado en `Fecha-I`.|
|`delay`|1 si `min_diff` > 15, 0 en caso contrario.|

## Desafío

### Instrucciones

1. Crea un repositorio en **GitHub** y copia todo el contenido del desafío en él. Recuerda que el repositorio debe ser **público**.

2. Usa la rama **main** para cualquier entrega oficial que debamos revisar. Se recomienda encarecidamente usar las prácticas de desarrollo [GitFlow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow). **NOTA: no elimines tus ramas de desarrollo.**

3. Por favor, no cambies la estructura del desafío (nombres de carpetas y archivos).

4. Toda la documentación y explicaciones que debas entregarnos deben ir en el archivo `challenge.md` dentro de la carpeta `docs`.

5. Para enviar tu desafío, debes hacer una solicitud `POST` a:
    `https://advana-challenge-check-api-cr-k4hdbggvoq-uc.a.run.app/software-engineer`
    Este es un ejemplo del cuerpo de la solicitud:
    ```json
    {
      "name": "Juan Perez",
      "mail": "juan.perez@example.com",
      "github_url": "https://github.com/juanperez/latam-challenge.git",
      "api_url": "https://juan-perez.api"
    }
    ```
    ##### ***POR FAVOR, ENVÍA LA SOLICITUD SOLO UNA VEZ.***

    Si tu solicitud fue exitosa, recibirás este mensaje:
    ```json
    {
      "status": "OK",
      "detail": "your request was received"
    }
    ```

***NOTA: Recomendamos enviar el desafío incluso si no lograste completar todas las partes.***

### Contexto:

Necesitamos operacionalizar el trabajo del científico de datos para el equipo del aeropuerto. Para ello, hemos decidido habilitar una `API` en la que puedan consultar la predicción de retraso de un vuelo.

*Recomendamos leer todo el desafío (todas sus partes) antes de comenzar a desarrollarlo.*

### Parte I

Para operacionalizar el modelo, transcribe el archivo `.ipynb` al archivo `model.py`:

- Si encuentras algún error, corrígelo.
- El DS propuso algunos modelos al final. Elige el mejor modelo a tu criterio y argumenta por qué. **No es necesario hacer mejoras al modelo.**
- Aplica todas las buenas prácticas de programación que consideres necesarias en este punto.
- El modelo debe pasar las pruebas ejecutando `make model-test`.

> **Nota:**
> - **No puedes** eliminar o cambiar el nombre o argumentos de los métodos **proporcionados**.
> - **Puedes** cambiar/completar la implementación de los métodos proporcionados.
> - **Puedes** crear las clases y métodos adicionales que consideres necesarios.

### Parte II

Despliega el modelo en una `API` con `FastAPI` usando el archivo `api.py`.

- La `API` debe pasar las pruebas ejecutando `make api-test`.

> **Nota:** 
> - **No puedes** usar otro framework.

### Parte III

Despliega la `API` en tu proveedor de nube favorito (recomendamos usar GCP).

- Coloca la URL de la `API` en el `Makefile` (línea 26).
- La `API` debe pasar las pruebas ejecutando `make stress-test`.

> **Nota:** 
> - **Es importante que la API esté desplegada hasta que revisemos las pruebas.**

### Parte IV

Estamos buscando una implementación adecuada de `CI/CD` para este desarrollo.

- Crea una nueva carpeta llamada `.github` y copia dentro de ella la carpeta `workflows` que te proporcionamos.
- Completa tanto `ci.yml` como `cd.yml` (considera lo que hiciste en las partes anteriores).
