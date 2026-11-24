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

    def test_calidad_global_se_cambia_por_la_fachada(self):
        original = self.f.calidad_global()
        self.f.establecer_calidad_global("720p")
        self.assertEqual(self.f.calidad_global(), "720p")
        self.f.establecer_calidad_global(original)

    def test_nombre_de_servicio_por_tipo(self):
        self.assertEqual(self.f.nombre_servicio("Pelicula"), "ServicioPeliculas")
        self.assertEqual(self.f.nombre_servicio("Serie"), "ServicioSeries")

    def test_registro_y_cache_parten_vacios(self):
        self.assertEqual(self.f.registro_de_accesos(), [])
        self.assertEqual(self.f.aciertos_de_cache(), 0)


if __name__ == "__main__":
    unittest.main()
