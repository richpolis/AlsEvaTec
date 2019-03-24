# Título del Proyecto

AlsEvaTec

### Descargar repositorio 📋
Proyecto en python 2.7

```
git clone https://github.com/richpolis/AlsEvaTec.git
```

### Instalar pip en Linux 📋
Si su distribución de Linux vino con Python ya instalado, debería poder instalar PIP usando el administrador de paquetes de su sistema. Esto es preferible ya que las versiones de Python instaladas en el sistema no funcionan muy bien con el script get-pip.py utilizado en Windows y Mac.

Herramienta de paquete avanzado (Python 2.x)
```
sudo apt-get install python-pip
```

### Instalar pip en Windows 📋
Las siguientes instrucciones deberían funcionar en Windows 7, Windows 8.1 y Windows 10:

Descargue el script del instalador get-pip.py. Si estás en Python 3.2, necesitarás esta versión de get-pip.py. De cualquier manera, haga clic derecho en el enlace y seleccione Guardar como y guárdelo en cualquier carpeta del pc, como su carpeta de Descargas.

Abra el símbolo del sistema y navegue hasta el archivo get-pip.py.

Ejecute el siguiente comando: python get-pip.py


### Instalar virtualenv para pip 📋

```
pip install virtualenv
```

## Instalación ⚙
```
cd AlsEvaTec
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Poner en marcha el servidor 🚀
```
python manage.py runserver
```

## API endpoints 🛠️

Las rutas son:

* [Albums](http://localhost:8000/api/albums/) - Albums
* [ArtistGroup](http://localhost:8000/api/artists/) - ArtistGroup

La API es en base a viewsets por lo tanto se maneja por los verbos de http. Ejemplos:

```
POST http//localhost:8000/api/<model>/ - Crea objecto
GET http//localhost:8000/api/<model>/  - Registra objectos
GET http//localhost:8000/api/<model>/<id>/ - Regresa un objecto en particular
PUT http//localhost:8000/api/<model>/<id>/ - Actualiza un objecto en particular 
PATCH http//localhost:8000/api/<model>/<id>/ - Actualiza parcialmente un objecto en particular 
DELETE http//localhost:8000/api<model>/<id>/ - Elimina un objecto en particular
```

Para aplicar busquedas las dos APIs responden a las siguientes condicionales
```
GET http//localhost:8000/api/<model>/?album=<nombre del album>  - Returna segun el model la busqueda por album
GET http//localhost:8000/api/<model>/?artist=<nombre del artista>  - Returna segun el model la busqueda por artista
```


## Servicios adicionales endpoints

Las rutas son:

* [RandomText](http://localhost:8000/random/text/)
* [SOAP Service](http://localhost:8000/service/soap/)
