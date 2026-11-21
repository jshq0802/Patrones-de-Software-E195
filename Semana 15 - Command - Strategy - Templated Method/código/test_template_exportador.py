import unittest
from contenido import Pelicula, Serie
from exportador_lista import ExportadorLista, ExportadorTexto, ExportadorCSV, ExportadorHTML


class TestTemplateExportador(unittest.TestCase):

    def setUp(self):
        self.contenidos = [Pelicula("Dune", 155), Serie("Dark", 60, 26)]

    def test_plantilla_es_abstracta(self):
        with self.assertRaises(TypeError):
            ExportadorLista()

    def test_texto_sigue_encabezado_filas_pie(self):
        s = ExportadorTexto().exportar("Mi lista", self.contenidos)
        self.assertTrue(s.startswith("LISTA: Mi lista"))
        self.assertIn("1. Dune | Pelicula | 155 min", s)
        self.assertIn("2. Dark | Serie | 60 min", s)
        self.assertTrue(s.endswith("Total: 2 titulos, 215 min"))

    def test_csv_tiene_cabecera_y_total(self):
        lineas = ExportadorCSV().exportar("Mi lista", self.contenidos).split("\n")
        self.assertEqual(lineas[0], "posicion,titulo,tipo,minutos")
        self.assertEqual(lineas[1], '1,"Dune",Pelicula,155')
        self.assertEqual(lineas[-1], "total,2,,215")

    def test_html_abre_y_cierra_la_lista(self):
        s = ExportadorHTML().exportar("Mi lista", self.contenidos)
        self.assertIn("<h1>Mi lista</h1>", s)
        self.assertIn("<li>Dune (Pelicula, 155 min)</li>", s)
        self.assertIn("</ol>", s)

    def test_mismo_esqueleto_para_los_tres_formatos(self):
        for clase in (ExportadorTexto, ExportadorCSV, ExportadorHTML):
            s = clase().exportar("L", self.contenidos)
            self.assertEqual(len(s.split("\n")) >= 4, True)
            self.assertLess(s.index("Dune"), s.index("Dark"))

    def test_lista_vacia_solo_encabezado_y_pie(self):
        s = ExportadorTexto().exportar("Vacia", [])
        self.assertIn("Total: 0 titulos, 0 min", s)

    def test_metodo_plantilla_no_se_redefine_en_subclases(self):
        for clase in (ExportadorTexto, ExportadorCSV, ExportadorHTML):
            self.assertNotIn("exportar", clase.__dict__)

    def test_extensiones_por_formato(self):
        self.assertEqual([c.extension for c in (ExportadorTexto, ExportadorCSV, ExportadorHTML)],
                         ["txt", "csv", "html"])


if __name__ == "__main__":
    unittest.main()
