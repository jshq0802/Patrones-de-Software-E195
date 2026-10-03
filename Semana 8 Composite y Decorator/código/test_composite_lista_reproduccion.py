
import unittest

from contenido import Pelicula, Serie
from lista_reproduccion import ElementoCatalogo, ContenidoHoja, ListaReproduccion


class TestCompositeListaReproduccion(unittest.TestCase):

    def setUp(self):
        self.pelicula = ContenidoHoja(Pelicula("Interestelar", 169))
        self.serie = ContenidoHoja(Serie("Breaking Bad", 47, numero_episodios=62))

    def test_01_hoja_y_lista_cumplen_la_misma_interfaz(self):
        lista = ListaReproduccion("Favoritos")
        self.assertIsInstance(self.pelicula, ElementoCatalogo)
        self.assertIsInstance(lista, ElementoCatalogo)

    def test_02_hoja_devuelve_su_propia_duracion(self):
        self.assertEqual(self.pelicula.obtener_duracion_total(), 169)

    def test_03_lista_suma_la_duracion_de_sus_elementos(self):
        lista = ListaReproduccion("Favoritos")
        lista.agregar(self.pelicula).agregar(self.serie)
        self.assertEqual(lista.obtener_duracion_total(), 169 + 47)

    def test_04_listas_anidadas_suman_su_duracion_de_forma_recursiva(self):
        sublista = ListaReproduccion("Maraton")
        sublista.agregar(self.serie)
        lista_principal = ListaReproduccion("Favoritos")
        lista_principal.agregar(self.pelicula).agregar(sublista)
        self.assertEqual(lista_principal.obtener_duracion_total(), 169 + 47)

    def test_05_quitar_elemento_actualiza_la_duracion_total(self):
        lista = ListaReproduccion("Favoritos")
        lista.agregar(self.pelicula).agregar(self.serie)
        lista.quitar(self.serie)
        self.assertEqual(lista.obtener_duracion_total(), 169)

    def test_06_mostrar_incluye_el_nombre_de_la_lista_y_sus_elementos(self):
        lista = ListaReproduccion("Favoritos")
        lista.agregar(self.pelicula)
        texto = lista.mostrar()
        self.assertIn("Favoritos", texto)
        self.assertIn("Interestelar", texto)


if __name__ == "__main__":
    unittest.main(verbosity=2)
