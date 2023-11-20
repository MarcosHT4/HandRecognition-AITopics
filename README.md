# HandRecognition - AI Topics
## Datos del estudiante 📝
* **Nombre:** Marcos Andrés Simon Ágreda
* **Código:** 56728
* **Carrera:** Ingeniería de Sistemas Computacionales
* **Curso:** Tópicos Selectos en Inteligencia Artificial

## Descripción del proyecto 📋

El proyecto consiste en la implementación de una API, cuyos endpoints, de forma general, brindan acceso a un modelo de reconocimiento de puntos de referencia, de un máximo de dos manos en una imagen; además de indicar si la mano detectada es la izquierda o la derecha.

La API está desarrollada en Python, haciendo uso de la librería FastAPI, y el modelo de reconocimiento de puntos de referencia es proporcionado por la librería MediaPipe, con su modelo MediaPipe Hand Landmarker.

Como un extra, se ha desarrollado una aplicación web, que hace uso de la API, para brindar una interfaz gráfica al usuario, y así poder hacer uso de la API de forma más amigable, la cual se encuentra en la carpeta `frontend`.

## Descripción de la API 🚀

La API cuenta con los siguientes endpoints:

* `/status`: Endpoint que devuelve el estado de la API, en caso de que esté activa, devuelve un mensaje de éxito, además de datos extra, como el nombre de la API, la versión y el nombre del modelo.
* `/predict`: Endpoint que recibe una imagen, y devuelve los puntos de referencia de las manos detectadas, el score de cada mano, el área que ocupa cada una de las manos, además de indicar si la mano detectada es la izquierda o la derecha. Por otro lado, devuelve información relevante sobre la ejecución del endpoint, como el tiempo de ejecución, el nombre y tamaño de la imagen, y la versión del modelo.
* `/annotate`: Endpoint que recibe una imagen, y devuelve la misma imagen, pero con anotaciones de los puntos de referencia de las manos detectadas, el score de cada mano, además de indicar si la mano detectada es la izquierda o la derecha.
* `/reports`: Endpoint que devuelve un reporte en formato .csv de la ejecución de los endpoints `/predict` y `/annotate`, proporcionando información relevante como: El nombre y tamaño de la imagen original, la predicción de cual mano es la izquierda y cual es la derecha, el score de cada mano, el área que ocupa cada una de las manos, el tiempo de ejecución, la fecha y hora de la ejecución, el tiempo de ejecución y la versión del modelo.

## Proceso de instalación y ejecución 🛠️

Para poder ejecutar la API, se debe tener instalado Python 3.10 o superior Posteriormente, se debe instalar las dependencias del proyecto, las cuales son:

```
numpy
fastapi
jupyter
uvicorn
opencv-python
mediapipe
lightning
Pillow
pydantic
pydantic_settings
python-multipart
```

Una vez instaladas, entrar al archivo `main.py`, y ejecutarlo. Esto iniciará el servidor de la API, el cual estará disponible en la dirección `http://localhost:8000`.

## Extra: Aplicación web 📦

Para poder ejecutar la aplicación web, se debe tener instalado Node.js 14 o superior. Posteriormente, se debe abrir la carpeta `frontend` en una terminal, y ejecutar el siguiente comando:

```
npm install
```

Posteriormente, crear un archivo `.env` en la carpeta `frontend`, y agregar la siguiente variable de entorno:

```
REACT_APP_BACKEND_URL=http://localhost:8000
``` 

Finalmente, ejecutar el siguiente comando:

```
npm start
```
