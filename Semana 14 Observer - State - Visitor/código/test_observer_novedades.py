import unittest

from observador_novedades import CanalNovedades, SuscriptorUsuario, RegistroNovedades, Novedad, Observador


class TestObserverNovedades(unittest.TestCase):

    def setUp(self):
        self.canal = CanalNovedades()
        self.ana = SuscriptorUsuario("Ana")
        self.luis = SuscriptorUsuario("Luis")
        self.novedad = Novedad("Dune 2", "Pelicula", "Ciencia ficcion")

    def test_01_todos_los_suscriptores_reciben_la_novedad(self):
        self.canal.suscribir(self.ana)
        self.canal.suscribir(self.luis)
        self.canal.publicar(self.novedad)
        self.assertEqual(self.ana.bandeja, [self.novedad])
        self.assertEqual(self.luis.bandeja, [self.novedad])

    def test_02_el_filtro_por_genero_solo_deja_pasar_lo_que_interesa(self):
        terror = SuscriptorUsuario("Tomas", generos=["Terror"])
        self.canal.suscribir(terror)
        self.canal.suscribir(self.ana)
        self.canal.publicar(self.novedad)
        self.assertEqual(terror.bandeja, [])
        self.assertEqual(len(self.ana.bandeja), 1)

    def test_03_quien_se_desuscribe_deja_de_recibir(self):
        self.canal.suscribir(self.ana)
        self.canal.desuscribir(self.ana)
        self.canal.publicar(self.novedad)
        self.assertEqual(self.ana.bandeja, [])

    def test_04_suscribir_dos_veces_no_duplica_los_avisos(self):
        self.canal.suscribir(self.ana)
        self.canal.suscribir(self.ana)
        self.canal.publicar(self.novedad)
        self.assertEqual(self.canal.total_observadores(), 1)
        self.assertEqual(len(self.ana.bandeja), 1)

    def test_05_observadores_de_distinto_tipo_conviven_en_el_mismo_canal(self):
        registro = RegistroNovedades()
        self.canal.suscribir(self.ana)
        self.canal.suscribir(registro)
        self.canal.publicar(self.novedad)
        self.assertEqual(registro.eventos, ["Pelicula nueva: Dune 2 (Ciencia ficcion)"])

    def test_06_se_puede_desuscribir_durante_la_notificacion(self):
        canal = self.canal

        class UnaVez(Observador):
            def __init__(self):
                self.recibidas = 0

            def actualizar(self, novedad):
                self.recibidas += 1
                canal.desuscribir(self)

        una_vez = UnaVez()
        canal.suscribir(una_vez)
        canal.suscribir(self.ana)
        canal.publicar(self.novedad)
        canal.publicar(self.novedad)
        self.assertEqual(una_vez.recibidas, 1)
        self.assertEqual(len(self.ana.bandeja), 2)

    def test_07_no_leidas_y_marcar_leidas(self):
        self.canal.suscribir(self.ana)
        self.canal.publicar(self.novedad)
        self.canal.publicar(Novedad("Dark 4", "Serie", "Misterio"))
        self.assertEqual(self.ana.no_leidas(), 2)
        self.ana.marcar_leidas()
        self.assertEqual(self.ana.no_leidas(), 0)

    def test_08_publicar_sin_observadores_no_falla(self):
        self.canal.publicar(self.novedad)
        self.assertEqual(self.canal.total_observadores(), 0)


if __name__ == "__main__":
    unittest.main()
