import unittest

from contenido import Pelicula, Serie
from lista_reproduccion import ListaReproduccion, ContenidoHoja


class TestIteratorLista(unittest.TestCase):

    def setUp(self):
        self.dune = Pelicula("Dune", 155)
        self.dark = Serie("Dark", 60, 26)
        self.inter = Pelicula("Interestelar", 169)
        self.crown = Serie("The Crown", 58, 60)
        self.interna = ListaReproduccion("Clasicos")
        self.interna.agregar(ContenidoHoja(self.inter)).agregar(ContenidoHoja(self.crown))
        self.lista = ListaReproduccion("Maraton")
        self.lista.agregar(ContenidoHoja(self.dune)).agregar(self.interna).agregar(ContenidoHoja(self.dark))

    def test_01_recorre_los_contenidos_en_orden(self):
        titulos = [c.titulo for c in self.lista.crear_iterador()]
        self.assertEqual(titulos, ["Dune", "Interestelar", "The Crown", "Dark"])

    def test_02_aplana_las_listas_anidadas(self):
        for contenido in self.lista.crear_iterador():
            self.assertNotIsInstance(contenido, ListaReproduccion)

    def test_03_hay_siguiente_y_se_agota_al_final(self):
        it = self.lista.crear_iterador()
        for _ in range(4):
            self.assertTrue(it.hay_siguiente())
            it.siguiente()
        self.assertFalse(it.hay_siguiente())
        with self.assertRaises(StopIteration):
            it.siguiente()

    def test_04_iterador_por_tipo_solo_entrega_ese_tipo(self):
        series = [c.titulo for c in self.lista.crear_iterador("Serie")]
        peliculas = [c.titulo for c in self.lista.crear_iterador("Pelicula")]
        self.assertEqual(series, ["The Crown", "Dark"])
        self.assertEqual(peliculas, ["Dune", "Interestelar"])

    def test_05_reiniciar_vuelve_al_principio(self):
        it = self.lista.crear_iterador()
        it.siguiente()
        it.siguiente()
        it.reiniciar()
        self.assertEqual(it.siguiente().titulo, "Dune")

    def test_06_dos_iteradores_son_independientes_y_no_alteran_la_lista(self):
        a = self.lista.crear_iterador()
        b = self.lista.crear_iterador()
        a.siguiente()
        a.siguiente()
        self.assertEqual(b.siguiente().titulo, "Dune")
        self.assertEqual(self.lista.obtener_duracion_total(), 155 + 169 + 58 + 60)

    def test_07_lista_vacia_no_tiene_siguiente_y_funciona_con_for(self):
        vacia = ListaReproduccion("Vacia")
        self.assertFalse(vacia.crear_iterador().hay_siguiente())
        self.assertEqual([c.titulo for c in self.lista], ["Dune", "Interestelar", "The Crown", "Dark"])


if __name__ == "__main__":
    unittest.main()
