# PYSC - Python Screen Capture CLI

Una herramienta de línea de comandos para realizar capturas de pantalla utilizando Python.

El programa permite:

- Capturar toda la pantalla o un monitor específico.
- Guardar la captura en distintos formatos de imagen.
- Esperar un tiempo antes de capturar.
- Listar todos los monitores conectados.
- Realizar capturas automáticamente cada vez que se hace clic con el mouse.

---

# Características

- Captura de pantalla completa.
- Selección de monitor.
- Modo "Click to Capture".
- Soporte para múltiples formatos de imagen.
- Creación automática de directorios.
- Nombres de archivo con fecha y hora.
- Numeración automática de capturas en modo continuo.
- Interfaz completamente desde la terminal.

---

# Requisitos

- Python 3.10 o superior

---

# Dependencias

Instalar las dependencias con:

```bash
pip install mss pynput
```

o bien

```bash
pip install -r requirements.txt
```

con el siguiente archivo `requirements.txt`:

```text
mss
pynput
```

---

# Uso básico

## Captura simple

```bash
python capture.py
```

Genera una captura de toda la pantalla y la guarda como:

```
capture_YYYYMMDD_HHMMSS.png
```

---

## Elegir nombre del archivo

```bash
python capture.py -o imagen.png
```

---

## Elegir formato

```bash
python capture.py -f jpg
```

Formatos disponibles:

- png
- jpg
- bmp
- gif
- tiff

---

# Seleccionar monitor

Primero listar los monitores disponibles:

```bash
python capture.py --list
```

Ejemplo:

```
[0] All: 3840x1080
[1] Monitor 1: 1920x1080
[2] Monitor 2: 1920x1080
```

Capturar únicamente el monitor 2:

```bash
python capture.py --monitor 2
```

---

# Retraso antes de capturar

Esperar 5 segundos antes de tomar la captura:

```bash
python capture.py --delay 5
```

---

# Modo Click-to-Capture

Este modo permanece escuchando los clics del mouse.

Cada clic izquierdo genera automáticamente una captura de pantalla.

```bash
python capture.py --loop
```

Las imágenes se guardarán como:

```
capture_20260713_201533_0000.png
capture_20260713_201534_0001.png
capture_20260713_201535_0002.png
...
```

Para finalizar:

```
Ctrl + C
```

---

# Elegir carpeta de salida

En modo continuo:

```bash
python capture.py --loop -o capturas
```

Las imágenes se guardarán dentro de:

```
capturas/
```

---

# Parámetros disponibles

| Parámetro | Descripción |
|------------|-------------|
| `-o`, `--output` | Archivo de salida o carpeta en modo loop |
| `-f`, `--format` | Formato de imagen |
| `-m`, `--monitor` | Monitor a capturar |
| `-l`, `--list` | Lista los monitores disponibles |
| `-d`, `--delay` | Espera antes de capturar |
| `--loop` | Activa el modo captura por clic |

---

# Ejemplos

Captura simple:

```bash
python capture.py
```

Capturar monitor 1:

```bash
python capture.py --monitor 1
```

Guardar como JPG:

```bash
python capture.py -f jpg
```

Esperar 10 segundos:

```bash
python capture.py --delay 10
```

Guardar con nombre personalizado:

```bash
python capture.py -o escritorio.png
```

Modo continuo:

```bash
python capture.py --loop
```

Modo continuo en una carpeta:

```bash
python capture.py --loop -o screenshots
```

---

# Funcionamiento interno

El programa utiliza dos bibliotecas principales:

### MSS

Se encarga de acceder directamente al framebuffer del sistema operativo para obtener la imagen de la pantalla de forma rápida y eficiente.

### pynput

Escucha los eventos del mouse para detectar cada clic cuando se utiliza el modo **Click-to-Capture**.

En modo continuo se crea una sesión de captura protegida mediante un `threading.Lock`, evitando conflictos si se producen varios eventos casi simultáneamente.

Cada imagen recibe automáticamente:

- fecha
- hora
- contador incremental

lo que evita sobrescribir capturas anteriores.

---

# Compatibilidad

Probado con:

- Windows
- Linux

También debería funcionar en macOS, aunque algunos permisos de accesibilidad pueden ser necesarios para que `pynput` pueda escuchar los eventos del mouse.

---

# Licencia

Este proyecto se distribuye bajo la licencia MIT.

Desarrollado por Emanuel Bellanti, año 2026.
