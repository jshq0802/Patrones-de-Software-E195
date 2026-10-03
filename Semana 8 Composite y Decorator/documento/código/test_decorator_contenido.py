"""Pruebas unitarias del patron Decorator (ContenidoDecorator y derivados).

Ejecucion: python -m unittest test_decorator_contenido.py -v
"""

import unittest

from contenido import Pelicula
from contenido_decorator import ConSubtitulos, ConAudioDescriptivo, ConMarcaDeAgua


class TestDecoratorContenido(unittest.TestCase):

    def setUp(self):
        self.pelicula = Pelicula("Interestelar", 169)

    def test_01_decorator_conserva_la_interfaz_contenido(self):
        decorado = ConSubtitulos(self.pelicula, "es")
        self.assertEqual(decorado.titulo, "Interestelar")
        self.assertEqual(decorado.tipo, "Pelicula")

    def test_02_subtitulos_agrega_el_idioma_al_mensaje(self):
        decorado = ConSubtitulos(self.pelicula, "es")
        self.assertIn("Subtitulos activados: es", decorado.reproducir())

    def test_03_audio_descriptivo_agrega_su_etiqueta(self):
        decorado = ConAudioDescriptivo(self.pelicula)
        self.assertIn("Audio descriptivo activado", decorado.reproducir())

    def test_04_decoradores_se_pueden_combinar_y_apilar(self):
        decorado = ConMarcaDeAgua(ConSubtitulos(self.pelicula, "en"), "PlataformaX")
        mensaje = decorado.reproducir()
        self.assertIn("Subtitulos activados: en", mensaje)
        self.assertIn("Marca de agua: PlataformaX", mensaje)

    def test_05_orden_de_decoradores_afecta_el_mensaje_pero_no_el_contenido_base(self):
        decorado_a = ConAudioDescriptivo(ConSubtitulos(self.pelicula, "es"))
        decorado_b = ConSubtitulos(ConAudioDescriptivo(self.pelicula), "es")
        self.assertIn("Interestelar", decorado_a.reproducir())
        self.assertIn("Interestelar", decorado_b.reproducir())

    def test_06_contenido_original_no_se_modifica_al_decorarlo(self):
        ConSubtitulos(self.pelicula, "es")
        self.assertNotIn("Subtitulos", self.pelicula.reproducir())


if __name__ == "__main__":
    unittest.main(verbosity=2)
