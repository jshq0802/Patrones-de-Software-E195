import unittest
from contenido import Pelicula, Serie
from ficha_contenido import FichaContenido
from estrategias_catalogo import (OrganizadorCatalogo, OrdenAlfabetico, OrdenDuracionCorta,
                                  OrdenDuracionLarga, OrdenPorGenero, OrdenOriginal, EstrategiaOrden)


def ficha(contenido, genero):
    f = FichaContenido()
    f.contenido_base = contenido
    f.genero = genero
    return f


class TestStrategyCatalogo(unittest.TestCase):

    def setUp(self):
        self.fichas = [
            ficha(Pelicula("Oppenheimer", 180), "Drama"),
            ficha(Serie("Dark", 60, 26), "Misterio"),
            ficha(Pelicula("Dune", 155), "Ciencia ficcion"),
        ]

    def titulos(self, fichas):
        return [f.contenido_base.titulo for f in fichas]

    def test_estrategia_es_abstracta(self):
        with self.assertRaises(TypeError):
            EstrategiaOrden()

    def test_orden_alfabetico(self):
        r = OrganizadorCatalogo(OrdenAlfabetico()).organizar(self.fichas)
        self.assertEqual(self.titulos(r), ["Dark", "Dune", "Oppenheimer"])

    def test_orden_duracion_corta(self):
        r = OrganizadorCatalogo(OrdenDuracionCorta()).organizar(self.fichas)
        self.assertEqual(self.titulos(r), ["Dark", "Dune", "Oppenheimer"])

    def test_orden_duracion_larga(self):
        r = OrganizadorCatalogo(OrdenDuracionLarga()).organizar(self.fichas)
        self.assertEqual(self.titulos(r), ["Oppenheimer", "Dune", "Dark"])

    def test_orden_por_genero(self):
        r = OrganizadorCatalogo(OrdenPorGenero()).organizar(self.fichas)
        self.assertEqual(self.titulos(r), ["Dune", "Oppenheimer", "Dark"])

    def test_orden_original_conserva_el_orden(self):
        r = OrganizadorCatalogo(OrdenOriginal()).organizar(self.fichas)
        self.assertEqual(self.titulos(r), ["Oppenheimer", "Dark", "Dune"])

    def test_cambiar_estrategia_en_tiempo_de_ejecucion(self):
        org = OrganizadorCatalogo(OrdenAlfabetico())
        primero = self.titulos(org.organizar(self.fichas))
        org.cambiar_estrategia(OrdenDuracionLarga())
        segundo = self.titulos(org.organizar(self.fichas))
        self.assertNotEqual(primero, segundo)
        self.assertIsInstance(org.estrategia_actual(), OrdenDuracionLarga)

    def test_no_modifica_la_lista_original(self):
        antes = self.titulos(self.fichas)
        OrganizadorCatalogo(OrdenAlfabetico()).organizar(self.fichas)
        self.assertEqual(self.titulos(self.fichas), antes)


if __name__ == "__main__":
    unittest.main()
