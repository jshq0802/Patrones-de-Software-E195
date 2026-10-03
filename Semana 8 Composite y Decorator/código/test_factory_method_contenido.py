"""Pruebas unitarias del patron Factory Method (Contenido / GestorContenidoService).

Ejecucion: python -m unittest test_factory_method_contenido.py -v
"""

import unittest

from contenido import Contenido, Pelicula, Serie
from gestor_contenido_service import (
    GestorContenidoService,
    ServicioPeliculas,
    ServicioSeries,
)
from configuracion_global import ConfiguracionGlobal


class TestFactoryMethodContenido(unittest.TestCase):

    def setUp(self):
        ConfiguracionGlobal._reiniciar_para_pruebas()

    def test_01_servicio_peliculas_crea_instancia_de_pelicula(self):
        servicio = ServicioPeliculas()
        contenido = servicio.crear_contenido("Interestelar", 169)
        self.assertIsInstance(contenido, Pelicula)

    def test_02_servicio_series_crea_instancia_de_serie(self):
        servicio = ServicioSeries()
        contenido = servicio.crear_contenido("Breaking Bad", 47, numero_episodios=62)
        self.assertIsInstance(contenido, Serie)

    def test_03_productos_cumplen_la_interfaz_contenido(self):
        pelicula = ServicioPeliculas().crear_contenido("Interestelar", 169)
        serie = ServicioSeries().crear_contenido("Breaking Bad", 47, numero_episodios=62)
        self.assertIsInstance(pelicula, Contenido)
        self.assertIsInstance(serie, Contenido)

    def test_04_reproducir_pelicula_devuelve_mensaje_esperado(self):
        pelicula = Pelicula("Interestelar", 169)
        self.assertIn("Interestelar", pelicula.reproducir())
        self.assertIn("sesion continua", pelicula.reproducir())

    def test_05_reproducir_serie_devuelve_mensaje_esperado(self):
        serie = Serie("Breaking Bad", 47, numero_episodios=62)
        mensaje = serie.reproducir()
        self.assertIn("Breaking Bad", mensaje)
        self.assertIn("62", mensaje)

    def test_06_publicar_contenido_usa_calidad_configurada(self):
        ConfiguracionGlobal.obtener_instancia().establecer_parametro("calidad_maxima", "720p")
        resultado = ServicioPeliculas().publicar_contenido("Interestelar", 169)
        self.assertIn("720p", resultado)

    def test_07_agregar_nuevo_creador_no_modifica_metodo_de_negocio(self):

        class Documental(Contenido):
            tipo = "Documental"

            def reproducir(self):
                return f"Reproduciendo el documental '{self.titulo}'."

        class ServicioDocumentales(GestorContenidoService):
            def crear_contenido(self, titulo, duracion_minutos, **kwargs):
                return Documental(titulo, duracion_minutos)

        resultado = ServicioDocumentales().publicar_contenido("Cosmos", 55)
        self.assertIn("Cosmos", resultado)
        self.assertIn("Documental", resultado)


if __name__ == "__main__":
    unittest.main(verbosity=2)
