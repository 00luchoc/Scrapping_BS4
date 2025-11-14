import sys
import json
import os
import re  # para limpiar el nombre del archivo
from newspaper import Article

def extraer_articulo_auto(url):
    """
    Descarga, procesa y extrae el contenido principal y metadatos.
    Devuelve un diccionario con los datos.
    """
    articulo = Article(url)
    
    # Descarga el HTML del artículo
    articulo.download()
    
    # Analiza el HTML para encontrar los datos
    articulo.parse()

    # Estructura los datos como un diccionario
    datos = {
        "titulo": articulo.title,
        "autor": ", ".join(articulo.authors),
        "fecha": articulo.publish_date.strftime('%Y-%m-%d') if articulo.publish_date else "No encontrada",
        "contenido": articulo.text
    }
    
    # Devuelve el DICCIONARIO
    return datos

def limpiar_filename(titulo):
    """
    Toma un título y lo convierte en un nombre de archivo seguro
    quitando caracteres inválidos.
    """
    # Elimina caracteres no válidos en nombres de archivo
    safe_name = re.sub(r'[<>:"/\\|?*]', '', titulo)
    # Reemplaza espacios por guiones bajos
    safe_name = safe_name.replace(' ', '_')
    # Limita la longitud a 100 caracteres para evitar errores
    return safe_name[:100] + ".json"

# --- Punto de entrada del script ---
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Se requiere una URL como argumento.")
        print("Uso: python scripts/script_auto.py <URL_DEL_ARTICULO>")
        sys.exit(1)
        
    url_ingresada = sys.argv[1]
    
    try:
        # 1. Extraer los datos (se recibe un dict)
        datos_articulo = extraer_articulo_auto(url_ingresada)
        
        # 2. Generar un nombre de archivo seguro desde el título
        if not datos_articulo.get("titulo"):
            nombre_archivo = "articulo_sin_titulo.json"
        else:
            nombre_archivo = limpiar_filename(datos_articulo["titulo"])
        
        # 3. Definir la ruta de guardado
        carpeta_salida = "data_output"
        # Asegura que la carpeta exista
        os.makedirs(carpeta_salida, exist_ok=True) 
        path_salida = os.path.join(carpeta_salida, nombre_archivo)
        
        # 4. Guardar el archivo JSON
        with open(path_salida, 'w', encoding='utf-8') as f:
            # Usa json.dump para escribir el dict como JSON
            json.dump(datos_articulo, f, indent=2, ensure_ascii=False)
        
        # 5. Imprime la confirmación
        print(f"¡Éxito! Artículo guardado en: {path_salida}")

    except Exception as e:
        print(f"Error al procesar o guardar la URL: {e}")
        sys.exit(1)