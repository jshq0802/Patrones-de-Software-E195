import unittest

from contenido import Pelicula
from lista_reproduccion import ListaReproduccion, ContenidoHoja
from mediador_reproduccion import (MediadorReproduccion, ControlReproduccion,
                                    ControlSubtitulos, ColaReproduccion, RegistroActividad)


def armar(lista=None):
    cola = ColaReproduccion()
    if lista is not None:
        cola.cargar(lista.crear_iterador())
    return MediadorReproduccion(ControlReproduccion(), ControlSubtitulos(), cola, RegistroActividad())


class TestMediatorReproduccion(unittest.TestCase):

    def setUp(self):
        self.a = Pelicula("Dune", 100)
        self.b = Pelicula("Interestelar", 50)
        self.lista = ListaReproduccion("Maraton")
        self.lista.agregar(ContenidoHoja(self.a)).agregar(ContenidoHoja(self.b))
        self.m = armar(self.lista)

    def test_01_reproducir_coordina_control_subtitulos_y_registro(self):
        self.m.subtitulos.establecer_idioma("es")
        self.m.reproducir(self.a)
        self.assertTrue(self.m.control.reproduciendo)
        texto = " ".join(self.m.registro.eventos)
        self.assertIn("Reproduciendo 'Dune'", texto)
        self.assertIn("Subtitulos en es", texto)

    def test_02_los_colegas_no_se_conocen_entre_si(self):
        for colega in (self.m.control, self.m.subtitulos, self.m.cola, self.m.registro):
            referencias = [v for v in vars(colega).values()
                           if isinstance(v, (ControlReproduccion, ControlSubtitulos,
                                             ColaReproduccion, RegistroActividad))]
            self.assertEqual(referencias, [])

    def test_03_pausar_sin_reproducir_no_hace_nada(self):
        self.m.control.pausar()
        self.assertEqual(self.m.registro.eventos, [])

    def test_04_al_terminar_un_titulo_pasa_al_siguiente_de_la_cola(self):
        self.m.cola.cargar(self.lista.crear_iterador())
        self.m.reproducir(self.m.cola.siguiente())
        self.m.control.avanzar(100)
        self.assertEqual(self.m.control.contenido.titulo, "Interestelar")
        self.assertTrue(self.m.control.reproduciendo)

    def test_05_al_terminar_la_ultima_registra_fin_de_la_lista(self):
        self.m.cola.cargar(self.lista.crear_iterador())
        self.m.reproducir(self.m.cola.siguiente())
        self.m.cola.solicitar_siguiente()
        self.m.control.avanzar(50)
        self.assertFalse(self.m.control.reproduciendo)
        self.assertIn("Fin de la lista.", self.m.registro.eventos)

    def test_06_cambiar_idioma_se_registra(self):
        self.m.subtitulos.establecer_idioma("en")
        self.assertEqual(self.m.subtitulos.idioma, "en")
        self.assertIn("Subtitulos en en.", self.m.registro.eventos)

    def test_07_siguiente_solicitado_sin_lista_cargada_no_falla(self):
        m = armar()
        m.cola.solicitar_siguiente()
        self.assertIn("Fin de la lista.", m.registro.eventos)

    def test_08_avanzar_no_pasa_de_la_duracion(self):
        m = armar()
        m.reproducir(self.a)
        m.control.avanzar(500)
        self.assertEqual(m.control.minuto, 100)


    def test_09_si_la_autorizacion_rechaza_no_reproduce_y_lo_registra(self):
        m = armar()
        m._autorizar = lambda c: (False, "edad")
        self.assertFalse(m.reproducir(self.a))
        self.assertFalse(m.control.reproduciendo)
        self.assertIn("Acceso denegado a 'Dune': edad", m.registro.eventos)

    def test_10_la_cola_omite_los_titulos_no_autorizados(self):
        m = armar(self.lista)
        m._autorizar = lambda c: (c.titulo != "Dune", "edad")
        m.cola.solicitar_siguiente()
        self.assertEqual(m.control.contenido.titulo, "Interestelar")


if __name__ == "__main__":
    unittest.main()
