import unittest
from facade_streaming import FachadaStreaming


class TestFachadaNuevosPatrones(unittest.TestCase):

    def setUp(self):
        self.f = FachadaStreaming()
        self.fichas = [self.f.publicar_pelicula("Zeta", 100, genero="Drama"),
                       self.f.publicar_serie("Alfa", 40, 10, genero="Accion")]
        self.lista = self.f.crear_lista_reproduccion("Mi lista", [])
        self.h = self.f.crear_historial_comandos()

    def test_agregar_deshacer_y_exportar(self):
        self.f.agregar_a_lista(self.h, self.lista, self.fichas[0])
        self.assertIn("Zeta", self.f.exportar_lista(self.lista, "Texto"))
        self.h.deshacer()
        self.assertIn("Total: 0", self.f.exportar_lista(self.lista, "Texto"))

    def test_quitar_y_vaciar_con_historial(self):
        for ficha in self.fichas:
            self.f.agregar_a_lista(self.h, self.lista, ficha)
        self.f.quitar_de_lista(self.h, self.lista, self.lista.elementos()[0])
        self.assertEqual(self.lista.cantidad(), 1)
        self.f.vaciar_lista(self.h, self.lista)
        self.h.deshacer()
        self.assertEqual(self.lista.cantidad(), 1)

    def test_ordenar_por_criterio(self):
        r = self.f.ordenar_catalogo(self.fichas, "Titulo (A-Z)")
        self.assertEqual(r[0].contenido_base.titulo, "Alfa")

    def test_criterio_desconocido_usa_orden_original(self):
        r = self.f.ordenar_catalogo(self.fichas, "inexistente")
        self.assertEqual(r, self.fichas)

    def test_formatos_disponibles(self):
        self.assertEqual(self.f.formatos_exportacion(), ["Texto", "CSV", "HTML"])


if __name__ == "__main__":
    unittest.main()
