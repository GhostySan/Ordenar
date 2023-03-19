import os
import shutil
import uuid
from tqdm import tqdm

# Lista de extensiones para cada tipo de archivo
carpetas = {"Comprimidos": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".z", ".cab", ".iso", ".img", ".dmg", ".jar", ".war", ".ear"],
            "Imagenes": [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".bmp", ".dib", ".svg", ".svgz", ".tif", ".tiff", ".webp", ".ico", ".icon", ".jxr", ".hdp", ".wdp", ".cur", ".dds", ".exr", ".hdr", ".jng", ".mng", ".pcx", ".pict", ".psd", ".psb", ".raw", ".arw", ".cr2", ".nrw", ".k25", ".kdc", ".dng", ".dcr", ".mos", ".pxn", ".raf", ".fff", ".3fr", ".qtk", ".rw2", ".sr2", ".srf", ".srw", ".x3f", ".avif", ".heic", ".heif", ".ai", ".eps"],
            "Audio": ['.aac', '.ac3', '.aiff', '.ape', '.au', '.dts', '.flac', '.m4a', '.m4b', '.m4p', '.mka', '.mp1', '.mp2', '.mp3', '.mpc', '.ogg', '.oma', '.pcm', '.ra', '.rm', '.tta', '.wav', '.wma', '.wv'],
            "Documentos": ['.doc', '.docx', '.dot', '.dotx', '.docm', '.dotm', '.rtf', '.odt', '.wpd', '.wps', '.xml', '.xps', '.mht', '.mhtml', '.txt', '.pdf', '.djvu', '.epub', '.fb2', '.mobi', '.pdb', '.prc', '.azw', '.azw3', '.cbz', '.cbr', '.cb7', '.cbt', '.cba', '.xps'],
            "Videos": ['.avi', '.mov', '.mp4', '.mpg', '.mpeg', '.flv', '.wmv', '.m4v', '.ts', '.mkv', '.webm', '.3gp', '.ogv', '.divx', '.xvid'],
            "Programas": [".exe", ".bat", ".cmd", ".com",".jse", ".msc", ".msi", ".msp", ".mst", ".pif", ".ps1", ".psm1",".pyc", ".pyo", ".reg", ".scr", ".vb", ".vbe", ".vbs", ".ws", ".wsc", ".wsf", ".wsh"],
            "Programacion": ['.py', '.pyc', '.pyd', '.pyw', '.pyo', '.pyx', '.pyi', '.pxd', '.pxi', '.pyz', '.pyzw', '.pywz', '.ipynb', '.html', '.css', '.js', '.json', '.xml', '.yaml', '.csv', '.ini', '.cfg', '.conf', '.md', '.rst'],
            "No clasificado": []}

# Ruta de la carpeta actual
ruta_actual = os.getcwd()

# Crear la carpeta "Ordenado"
ruta_ordenado = os.path.join(ruta_actual, "Ordenado")
if not os.path.exists(ruta_ordenado):
    os.mkdir(ruta_ordenado)

# Crear la carpeta "Carpetas" dentro de la carpeta "Ordenado"
ruta_carpetas = os.path.join(ruta_ordenado, "Carpetas")
if not os.path.exists(ruta_carpetas):
    os.mkdir(ruta_carpetas)

# Obtener la lista de archivos y carpetas en la carpeta actual
archivos = os.listdir(ruta_actual)

# Definir el número total de archivos que se van a mover
num_archivos = len([archivo for archivo in archivos if archivo != "Ordenado" and archivo != "Ordenar.exe"])

# Mostrar la barra de progreso
pbar = tqdm(total=len(archivos), desc="Moviendo archivos")
# Mover los archivos a sus respectivas subcarpetas
for archivo in archivos:
    # Excluir la carpeta "Ordenado" y el archivo "ordenar.py"
    if archivo != "Ordenado" and archivo != "Ordenar.exe":
        ruta_archivo = os.path.join(ruta_actual, archivo)
        # Si es una carpeta, moverla a la carpeta "Carpetas"
        if os.path.isdir(ruta_archivo):
            nuevo_nombre = archivo
            i = 1
            # Agregar un sufijo numérico al nombre si ya existe en la carpeta destino
            while os.path.exists(os.path.join(ruta_carpetas, nuevo_nombre)):
                nuevo_nombre = f"{archivo}_{i}"
                i += 1
            shutil.move(ruta_archivo, os.path.join(ruta_carpetas, nuevo_nombre))
        # Si es un archivo, moverlo a su subcarpeta correspondiente
        else:
            # Obtener la extensión del archivo
            extension = os.path.splitext(ruta_archivo)[1]
            # Buscar la subcarpeta correspondiente
            carpeta_encontrada = False
            for carpeta, extensiones in carpetas.items():
                if extension in extensiones:
                    ruta_subcarpeta = os.path.join(ruta_ordenado, carpeta)
                    if not os.path.exists(ruta_subcarpeta):
                        os.mkdir(ruta_subcarpeta)
                    nuevo_nombre = archivo
                    i = 1
                    # Agregar un sufijo numérico al nombre si ya existe en la carpeta destino
                    while os.path.exists(os.path.join(ruta_subcarpeta, nuevo_nombre)):
                        nuevo_nombre = f"{os.path.splitext(archivo)[0]}_{uuid.uuid4().hex}{os.path.splitext(archivo)[1]}"
                        # Se utiliza uuid para generar un identificador aleatorio para el nombre del archivo
                        # de esta forma se evita posibles colisiones
                    shutil.move(ruta_archivo, os.path.join(ruta_subcarpeta, nuevo_nombre))
                    carpeta_encontrada = True
                    break
            # Si no se encontró una carpeta correspondiente, mover el archivo a la carpeta "No clasificado"
            if not carpeta_encontrada:
                ruta_no_clasificado = os.path.join(ruta_ordenado, "No clasificado")
                if not os.path.exists(ruta_no_clasificado):
                    os.mkdir(ruta_no_clasificado)
                nuevo_nombre = archivo
                i = 1
                # Agregar un sufijo numérico al nombre si ya existe en la carpeta destino
                while os.path.exists(os.path.join(ruta_no_clasificado, nuevo_nombre)):
                    nuevo_nombre = f"{os.path.splitext(archivo)[0]}_{uuid.uuid4().hex}{os.path.splitext(archivo)[1]}"
                    # Se utiliza uuid para generar un identificador aleatorio para el nombre del archivo
                    # de esta forma se evita posibles colisiones

                # Verificar si el nombre del archivo coincide con uno de la carpeta origen
                if nuevo_nombre in archivos:
                    nuevo_nombre = f"{uuid.uuid4().hex}{os.path.splitext(archivo)[1]}"

                shutil.move(ruta_archivo, os.path.join(ruta_no_clasificado, nuevo_nombre))
            # Incrementar la barra de progreso
            pbar.update(1)
            # Mostrar un mensaje de confirmación
print("Proceso completado.")
print("Presione cualquier tecla para salir...")
input()
      