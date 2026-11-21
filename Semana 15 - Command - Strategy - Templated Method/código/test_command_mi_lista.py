import unittest
from contenido import Pelicula, Serie
from lista_reproduccion import ListaReproduccion, ContenidoHoja
from comandos_mi_lista import AgregarALista, QuitarDeLista, VaciarLista, HistorialComandos, ComandoLista


class TestCommandMiLista(unittest.TestCase):

    def setUp(self):
        self.lista = ListaReproduccion("Mi lista")
        self.h = HistorialComandos()
        self.a = ContenidoHoja(Pelicula("Dune", 155))
        self.b = ContenidoHoja(Serie("Dark", 60, 26))
        self.c = ContenidoHoja(Pelicula("Oppenheimer", 180))

    def test_comando_es_abstracto(self):
        with self.assertRaises(TypeError):
            ComandoLista()

    def test_ejecutar_agrega_a_la_lista(self):
        self.h.ejecutar(AgregarALista(self.lista, self.a, "Dune"))
        self.assertEqual(self.lista.cantidad(), 1)

    def test_deshacer_agregar_quita_el_elemento(self):
        self.h.ejecutar(AgregarALista(self.lista, self.a, "Dune"))
        self.h.deshacer()
        self.assertEqual(self.lista.cantidad(), 0)

    def test_rehacer_vuelve_a_agregar(self):
        self.h.ejecutar(AgregarALista(self.lista, self.a, "Dune"))
        self.h.deshacer()
        self.h.rehacer()
        self.assertEqual(self.lista.cantidad(), 1)

    def test_deshacer_quitar_restaura_la_posicion_original(self):
        for e, t in ((self.a, "Dune"), (self.b, "Dark"), (self.c, "Oppenheimer")):
            self.h.ejecutar(AgregarALista(self.lista, e, t))
        self.h.ejecutar(QuitarDeLista(self.lista, self.b, "Dark"))
        self.assertEqual(self.lista.elementos(), [self.a, self.c])
        self.h.deshacer()
        self.assertEqual(self.lista.elementos(), [self.a, self.b, self.c])

    def test_vaciar_y_deshacer_restaura_todo_en_orden(self):
        for e, t in ((self.a, "Dune"), (self.b, "Dark")):
            self.h.ejecutar(AgregarALista(self.lista, e, t))
        self.h.ejecutar(VaciarLista(self.lista))
        self.assertEqual(self.lista.cantidad(), 0)
        self.h.deshacer()
        self.assertEqual(self.lista.elementos(), [self.a, self.b])

    def test_nueva_accion_invalida_el_rehacer(self):
        self.h.ejecutar(AgregarALista(self.lista, self.a, "Dune"))
        self.h.deshacer()
        self.h.ejecutar(AgregarALista(self.lista, self.b, "Dark"))
        self.assertFalse(self.h.puede_rehacer())

    def test_deshacer_sin_historial_no_falla(self):
        self.assertIsNone(self.h.deshacer())
        self.assertIsNone(self.h.rehacer())

    def test_registro_describe_las_acciones(self):
        self.h.ejecutar(AgregarALista(self.lista, self.a, "Dune"))
        self.h.ejecutar(QuitarDeLista(self.lista, self.a, "Dune"))
        self.assertEqual(self.h.registro(), ["Agregar 'Dune'", "Quitar 'Dune'"])


if __name__ == "__main__":
    unittest.main()
