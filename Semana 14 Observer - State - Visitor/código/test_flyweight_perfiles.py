import unittest

from flyweight_perfiles import FabricaPerfiles, SesionReproduccion


class TestFlyweightPerfiles(unittest.TestCase):

    def setUp(self):
        self.fabrica = FabricaPerfiles()

    def test_01_misma_calidad_devuelve_la_misma_instancia(self):
        self.assertIs(self.fabrica.obtener("4K"), self.fabrica.obtener("4K"))

    def test_02_calidades_distintas_son_instancias_distintas(self):
        self.assertIsNot(self.fabrica.obtener("720p"), self.fabrica.obtener("1080p"))

    def test_03_mil_sesiones_comparten_un_unico_perfil(self):
        perfil = self.fabrica.obtener("1080p")
        sesiones = [SesionReproduccion(f"u{i}", "Dune", i, self.fabrica.obtener("1080p"))
                    for i in range(1000)]
        self.assertTrue(all(s.perfil is perfil for s in sesiones))
        self.assertEqual(self.fabrica.total_perfiles_creados(), 1)

    def test_04_el_estado_extrinseco_es_propio_de_cada_sesion(self):
        perfil = self.fabrica.obtener("4K")
        s1 = SesionReproduccion("ana", "Dune", 10, perfil)
        s2 = SesionReproduccion("luis", "Dark", 55, perfil)
        self.assertIn("ana", s1.describir())
        self.assertIn("luis", s2.describir())
        self.assertIs(s1.perfil, s2.perfil)

    def test_05_el_perfil_es_inmutable(self):
        perfil = self.fabrica.obtener("4K")
        with self.assertRaises(AttributeError):
            perfil.bitrate_kbps = 1

    def test_06_calidad_no_soportada_lanza_error(self):
        with self.assertRaises(ValueError):
            self.fabrica.obtener("8K")


if __name__ == "__main__":
    unittest.main()
