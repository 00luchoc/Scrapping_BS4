import sys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# CONFIG GENERAL POR SUPERMERCADO
CONFIG_SITIOS = {
    "DIA": {
        "base_url": "https://diaonline.supermercadosdia.com.ar"
    },
    "COTO": {
        "base_url": "https://www.cotodigital.com.ar/sitios/cdigi/nuevositio"
    },
    "Carrefour": {
        "base_url": "https://www.carrefour.com.ar"
    }
}

# CONFIGURAR DRIVER
def configurar_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


# PARSEADOR ROBUSTO POR XPATH
def parsear_pagina_vtex(driver, supermercado):
    productos = []

    time.sleep(2)

    # 1) Selector principal: LINK de producto que contiene href y texto
    cards = driver.find_elements(
        By.XPATH,
        "//a[contains(@href,'/p') or contains(@href,'/producto') or contains(@href,'/product')]"
    )

    # 2) Segundo intento (por si usan otra estructura)
    if not cards:
        print("[INFO] Segundo intento de búsqueda…")
        cards = driver.find_elements(
            By.XPATH,
            "//div[contains(@class,'product')]//a"
        )

    if not cards:
        print("[ERROR] No se encontraron productos en esta tienda.")
        return []

    for card in cards:
        try:
            url = card.get_attribute("href") or ""
            nombre = (card.text or "").strip()
        except:
            continue

        # Precio: cualquier elemento que contenga "$"
        try:
            precio_elem = card.find_element(
                By.XPATH,
                ".//*[contains(text(), '$')]"
            )
            precio = precio_elem.text.strip()
        except:
            precio = "No disponible"

        if not nombre:
            continue

        productos.append({
            "Supermercado": supermercado,
            "Producto": nombre,
            "Precio": precio,
            "URL": url
        })

    return productos

# PROCESO PRINCIPAL
def main(termino_busqueda):
    print(f"--- Iniciando extracción para el término: '{termino_busqueda}' ---")

    driver = configurar_driver()
    todos_los_productos = []

    try:
        for nombre_super, config in CONFIG_SITIOS.items():

            url_busqueda = f"{config['base_url']}/{termino_busqueda}?map=ft"
            print(f"\n[INFO] Accediendo a: {nombre_super} ({url_busqueda})")

            driver.get(url_busqueda)
            time.sleep(4)

            # Avisos
            print("\n[PAUSA] El script está en pausa.")
            print("        >> 1. Mira la ventana de Chrome.")
            if nombre_super == "COTO":
                print("        >> IMPORTANTE: Seleccionar sucursal o continuar como invitado.")
            else:
                print("        >> Cerrá popups de cookies / ubicación.")
            print("        >> 3. Espera a que se carguen los productos.")
            input("        >> 4. Presiona ENTER aquí para continuar...")

            print("[INFO] Extrayendo productos…")

            productos = parsear_pagina_vtex(driver, nombre_super)

            if not productos:
                print(f"[INFO] No se extrajeron productos de {nombre_super}.")
            else:
                print(f"[INFO] Se extrajeron {len(productos)} productos de {nombre_super}.")
                todos_los_productos.extend(productos)

    except Exception as e:
        print(f"[ERROR GRAVE] {e}")

    finally:
        driver.quit()
        print("\n[INFO] Navegador cerrado.")

    # Guardar CSV
    if not todos_los_productos:
        print("\n[FINAL] No se extrajo ningún producto.")
        return

    df = pd.DataFrame(todos_los_productos)
    df.drop_duplicates(subset=["Supermercado", "Producto", "URL"], inplace=True)

    carpeta = "data_output"
    os.makedirs(carpeta, exist_ok=True)
    ruta_csv = os.path.join(carpeta, "precios_competencia.csv")

    df.to_csv(ruta_csv, index=False, encoding="utf-8-sig")

    print("\n--- ¡Proceso finalizado! ---")
    print(f"Total de productos: {len(df)}")
    print(f"Archivo guardado en: {ruta_csv}")

# ENTRY POINT
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python script.py \"leche\"")
        sys.exit(1)

    termino = sys.argv[1]
    main(termino)