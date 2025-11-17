import pytest
from script import parsear_pagina_vtex, configurar_driver, CONFIG_SITIOS

# -------- TESTS --------

def test_parsear_carrefour():
    driver = configurar_driver()

    # Ir a Carrefour y esperar la carga
    url = CONFIG_SITIOS["Carrefour"]["base_url"]
    driver.get(url)
    driver.implicitly_wait(8)

    productos = parsear_pagina_vtex(driver, "Carrefour")

    assert isinstance(productos, list)
    assert len(productos) > 0  # Al menos 1 producto encontrado
    assert "Producto" in productos[0]
    assert "Precio" in productos[0]
    assert "URL" in productos[0]

    driver.quit()

def test_parsear_sin_productos():
    driver = configurar_driver()
    productos = parsear_pagina_vtex(driver, "Carrefour")

    assert productos == []
