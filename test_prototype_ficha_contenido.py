"""Pruebas unitarias del patron Prototype (FichaContenido.clonar()).

Ejecucion: python -m unittest test_prototype_ficha_contenido.py -v
"""

import unittest

from configuracion_global import ConfiguracionGlobal
from gestor_contenido_service import ServicioPeliculas
from ficha_contenido_builder import FichaContenidoBuilderEstandar, CatalogoDirector


class TestPrototypeFichaContenido(unittest.TestCase):

    def setUp(self):
        ConfiguracionGlobal._reiniciar_para_pruebas()
        pelicula = ServicioPeliculas().crear_contenido("Interestelar", 169)
        director = CatalogoDirector(FichaContenidoBuilderEstandar())
        self.ficha_original = director.construir_ficha_completa(
            contenido_base=pelicula,
            sinopsis="Sinopsis original.",
            genero="Ciencia ficcion",
            clasificacion_audiencia="13+",
            anio_lanzamiento=2014,
            idiomas_disponibles=["es", "en"],
            subtitulos_disponibles=["es"],
            reparto=["Actor A", "Actor B"],
            director_obra="Directora X",
        )

    def test_01_clon_es_una_instancia_independiente(self):
        clon = self.ficha_original.clonar()
        self.assertIsNot(clon, self.ficha_original)

    def test_02_clon_conserva_los_valores_del_original(self):
        clon = self.ficha_original.clonar()
        self.assertEqual(clon.sinopsis, self.ficha_original.sinopsis)
        self.assertEqual(clon.genero, self.ficha_original.genero)
        self.assertEqual(clon.clasificacion_audiencia, self.ficha_original.clasificacion_audiencia)
        self.assertEqual(clon.idiomas_disponibles, self.ficha_original.idiomas_disponibles)

    def test_03_clon_comparte_el_mismo_contenido_base(self):
        """El contenido audiovisual es el mismo; solo cambia la metadata regional."""
        clon = self.ficha_original.clonar()
        self.assertIs(clon.contenido_base, self.ficha_original.contenido_base)

    def test_04_modificar_idiomas_del_clon_no_afecta_al_original(self):
        clon = self.ficha_original.clonar()
        clon.idiomas_disponibles.append("fr")
        self.assertNotIn("fr", self.ficha_original.idiomas_disponibles)

    def test_05_modificar_reparto_del_original_no_afecta_a_un_clon_ya_creado(self):
        clon = self.ficha_original.clonar()
        self.ficha_original.reparto.append("Actor C")
        self.assertNotIn("Actor C", clon.reparto)

    def test_06_clonacion_permite_crear_una_variante_regional_sin_reconstruir(self):
        clon_regional = self.ficha_original.clonar()
        clon_regional.clasificacion_audiencia = "16+"
        clon_regional.idiomas_disponibles = ["en"]

        self.assertEqual(self.ficha_original.clasificacion_audiencia, "13+")
        self.assertEqual(self.ficha_original.idiomas_disponibles, ["es", "en"])
        self.assertEqual(clon_regional.clasificacion_audiencia, "16+")
        self.assertEqual(clon_regional.idiomas_disponibles, ["en"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
