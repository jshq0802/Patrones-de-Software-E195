import unittest

from contenido import Pelicula, Serie
from contenido_decorator import ConSubtitulos
from lista_reproduccion import ListaReproduccion, ContenidoHoja
from visitante_catalogo import Visitante, VisitanteReporte, VisitanteCostoLicencias


class TestVisitorCatalogo(unittest.TestCase):

    def setUp(self):
        self.dune = Pelicula("Dune", 155)
        self.dark = Serie("Dark", 60, 26)
        self.crown = Serie("The Crown", 58, 60)
        interna = ListaReproduccion("Clasicos")
        interna.agregar(ContenidoHoja(self.crown))
        self.lista = ListaReproduccion("Maraton")
        self.lista.agregar(ContenidoHoja(self.dune)).agregar(ContenidoHoja(self.dark)).agregar(interna)

    def test_01_el_reporte_cuenta_peliculas_series_y_episodios(self):
        r = VisitanteReporte()
        self.lista.aceptar(r)
        self.assertEqual((r.peliculas, r.series, r.episodios), (1, 2, 86))

    def test_02_el_reporte_suma_los_minutos_totales_de_contenido(self):
        r = VisitanteReporte()
        self.lista.aceptar(r)
        self.assertEqual(r.minutos_totales, 155 + 60 * 26 + 58 * 60)

    def test_03_recorre_listas_anidadas(self):
        r = VisitanteReporte()
        self.lista.aceptar(r)
        self.assertEqual(r.listas, 2)

    def test_04_el_costo_de_licencias_usa_tarifa_por_pelicula_y_por_episodio(self):
        v = VisitanteCostoLicencias()
        self.lista.aceptar(v)
        self.assertEqual(v.total, 12.0 + 2.0 * 26 + 2.0 * 60)
        self.assertIn(("Dune", 12.0), v.detalle)

    def test_05_se_pueden_agregar_operaciones_nuevas_sin_tocar_las_clases(self):
        class Largos(Visitante):
            def __init__(self):
                self.titulos = []

            def visitar_pelicula(self, p):
                if p.duracion_minutos > 150:
                    self.titulos.append(p.titulo)

            def visitar_serie(self, s):
                pass

        v = Largos()
        self.lista.aceptar(v)
        self.assertEqual(v.titulos, ["Dune"])

    def test_06_un_contenido_decorado_se_visita_como_su_tipo_base(self):
        decorado = ConSubtitulos(self.dune, "es")
        r = VisitanteReporte()
        decorado.aceptar(r)
        self.assertEqual(r.peliculas, 1)

    def test_07_doble_despacho_cada_tipo_llama_a_su_metodo(self):
        llamadas = []

        class Espia(Visitante):
            def visitar_pelicula(self, p):
                llamadas.append("pelicula")

            def visitar_serie(self, s):
                llamadas.append("serie")

        self.dune.aceptar(Espia())
        self.dark.aceptar(Espia())
        self.assertEqual(llamadas, ["pelicula", "serie"])

    def test_08_lista_vacia_da_reporte_en_cero(self):
        r = VisitanteReporte()
        ListaReproduccion("Vacia").aceptar(r)
        self.assertEqual((r.peliculas, r.series, r.minutos_totales), (0, 0, 0))


if __name__ == "__main__":
    unittest.main()
