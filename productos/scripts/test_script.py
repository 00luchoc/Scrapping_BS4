import pytest
from script import parsear_pagina_vtex

# Objetos simples para simular Selenium
class FakeElem:
    def __init__(self, text, href, price=None):
        self.text = text
        self.href = href
        self.price = price

    def get_attribute(self, attr):
        return self.href if attr == "href" else None

    def find_element(self, *args, **kwargs):
        if self.price is not None:
            return FakeElem(self.price, None)
        raise Exception("no price")

class FakeDriver:
    def __init__(self, elems):
        self.elems = elems

    def find_elements(self, *args, **kwargs):
        return self.elems


# -------- TESTS --------

def test_parsear_ok():
    driver = FakeDriver([
        FakeElem("Yerba Playadito", "http://x.com/p1", "$4500")
    ])

    productos = parsear_pagina_vtex(driver, "COTO")

    assert len(productos) == 1
    assert productos[0]["Producto"] == "Yerba Playadito"
    assert productos[0]["Precio"] == "$4500"
    assert productos[0]["URL"] == "http://x.com/p1"


def test_parsear_sin_precio():
    driver = FakeDriver([
        FakeElem("Arroz Gallo", "http://x.com/p2", None)
    ])

    productos = parsear_pagina_vtex(driver, "DIA")

    assert productos[0]["Precio"] == "No disponible"


def test_parsear_sin_productos():
    driver = FakeDriver([])

    productos = parsear_pagina_vtex(driver, "Carrefour")

    assert productos == []
