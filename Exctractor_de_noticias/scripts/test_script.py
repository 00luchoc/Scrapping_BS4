import pytest
from script import extraer_articulo_auto, limpiar_filename
-
# TEST limpiar_filename()

def test_limpiar_filename_caracteres_invalidos():
    titulo = 'Hola: Qué tal? *Titulo* | Invalido / \\ <>'
    resultado = limpiar_filename(titulo)

    # No tiene que contener caracteres ilegales
    for c in ':?*|/\\<>':
        assert c not in resultado

    # Termina en .json
    assert resultado.endswith(".json")


def test_limpiar_filename_reemplazo_y_longitud():
    titulo = "a" * 200
    resultado = limpiar_filename(titulo)

    # largo = 100 caracteres + ".json"
    assert len(resultado) == 105
    assert resultado.endswith(".json")

# TEST extraer_articulo_auto()
# Simulacion newspaper.Article para que funcione sin internet.

class FakeArticle:
    def __init__(self, url):
        self.url = url
        self.title = "Título simulado"
        self.authors = ["Autor 1", "Autor 2"]
        self.publish_date = None
        self.text = "Contenido de ejemplo."

    def download(self):
        pass

    def parse(self):
        pass


def test_extraer_articulo_auto(monkeypatch):
    # Reemplaza Article por FakeArticle dentro del módulo
    monkeypatch.setattr("script.Article", FakeArticle)

    datos = extraer_articulo_auto("http://fakeurl.com/articulo")

    assert datos["titulo"] == "Título simulado"
    assert datos["autor"] == "Autor 1, Autor 2"
    assert datos["fecha"] == "No encontrada" 
    assert datos["contenido"] == "Contenido de ejemplo."
