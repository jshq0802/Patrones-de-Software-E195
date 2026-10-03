"""Pruebas unitarias del patron Abstract Factory (configuracion regional).

Ejecucion: python -m unittest test_abstract_factory_configuracion_regional.py -v
"""

import unittest

from configuracion_global import ConfiguracionGlobal
from gestor_contenido_service import ServicioPeliculas
from configuracion_regional import (
    FabricaConfiguracionRegional,
    FabricaConfiguracionLatam,
    FabricaConfiguracionUSA,
)
from ficha_contenido_builder import FichaContenidoBuilderEstandar, CatalogoDirector


class TestAbstractFactoryConfiguracionRegional(unittest.TestCase):

    def setUp(self):
        ConfiguracionGlobal._reiniciar_para_pruebas()
        self.pelicula = ServicioPeliculas().crear_contenido("Interestelar", 169)

    def test_01_fabrica_latam_crea_politica_y_idiomas_correctos(self):
        fabrica = FabricaConfiguracionLatam()
        politica = fabrica.crear_politica_clasificacion()
        idiomas = fabrica.crear_configuracion_idiomas()
        self.assertIn("RCC", politica.obtener_clasificacion_por_defecto())
        self.assertEqual(idiomas.obtener_idioma_principal(), "es")
        self.assertEqual(idiomas.obtener_idiomas_secundarios(), ["en", "pt"])

    def test_02_fabrica_usa_crea_politica_y_idiomas_correctos(self):
        fabrica = FabricaConfiguracionUSA()
        politica = fabrica.crear_politica_clasificacion()
        idiomas = fabrica.crear_configuracion_idiomas()
        self.assertIn("MPAA", politica.obtener_clasificacion_por_defecto())
        self.assertEqual(idiomas.obtener_idioma_principal(), "en")
        self.assertEqual(idiomas.obtener_idiomas_secundarios(), ["es"])

    def test_03_familias_de_fabricas_distintas_no_se_mezclan(self):
        idiomas_latam = FabricaConfiguracionLatam().crear_configuracion_idiomas()
        idiomas_usa = FabricaConfiguracionUSA().crear_configuracion_idiomas()
        self.assertNotEqual(idiomas_latam.obtener_idioma_principal(), idiomas_usa.obtener_idioma_principal())

    def test_04_director_construye_ficha_regional_con_fabrica_latam(self):
        director = CatalogoDirector(FichaContenidoBuilderEstandar())
        ficha = director.construir_ficha_regional(
            contenido_base=self.pelicula,
            fabrica_regional=FabricaConfiguracionLatam(),
            sinopsis="Edicion Latam",
            genero="Ciencia ficcion",
        )
        self.assertIn("RCC", ficha.clasificacion_audiencia)
        self.assertEqual(ficha.idiomas_disponibles, ["es", "en", "pt"])

    def test_05_director_construye_ficha_regional_con_fabrica_usa(self):
        director = CatalogoDirector(FichaContenidoBuilderEstandar())
        ficha = director.construir_ficha_regional(
            contenido_base=self.pelicula,
            fabrica_regional=FabricaConfiguracionUSA(),
            sinopsis="US edition",
            genero="Sci-Fi",
        )
        self.assertIn("MPAA", ficha.clasificacion_audiencia)
        self.assertEqual(ficha.idiomas_disponibles, ["en", "es"])

    def test_06_cliente_funciona_con_cualquier_fabrica_concreta(self):
        """El Director solo depende de la abstraccion FabricaConfiguracionRegional (DIP)."""

        def construir_con_fabrica(fabrica: FabricaConfiguracionRegional):
            director = CatalogoDirector(FichaContenidoBuilderEstandar())
            return director.construir_ficha_regional(self.pelicula, fabrica)

        ficha_latam = construir_con_fabrica(FabricaConfiguracionLatam())
        ficha_usa = construir_con_fabrica(FabricaConfiguracionUSA())
        self.assertNotEqual(ficha_latam.clasificacion_audiencia, ficha_usa.clasificacion_audiencia)


if __name__ == "__main__":
    unittest.main(verbosity=2)
