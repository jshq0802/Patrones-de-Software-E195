import dataclasses
import unittest

from contenido import Pelicula
from mediador_reproduccion import (MediadorReproduccion, ControlReproduccion,
                                    ControlSubtitulos, ColaReproduccion, RegistroActividad)
from memento_reproduccion import MementoReproduccion, HistorialPuntos


def armar():
    return MediadorReproduccion(ControlReproduccion(), ControlSubtitulos(),
                                ColaReproduccion(), RegistroActividad())


class TestMementoReproduccion(unittest.TestCase):

    def setUp(self):
        self.a = Pelicula("Dune", 100)
        self.b = Pelicula("Interestelar", 120)
        self.m = armar()

    def test_01_el_memento_es_inmutable(self):
        memento = MementoReproduccion(self.a, 30)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            memento.minuto = 99

    def test_02_pausar_guarda_el_punto_y_reproducir_continua_desde_ahi(self):
        self.m.reproducir(self.a)
        self.m.control.avanzar(40)
        self.m.control.pausar()
        self.m.reproducir(self.a)
        self.assertEqual(self.m.control.minuto, 40)
        self.assertIn("Se recupero el punto guardado de 'Dune'.", self.m.registro.eventos)

    def test_03_cada_titulo_guarda_su_propio_punto(self):
        self.m.reproducir(self.a)
        self.m.control.avanzar(10)
        self.m.control.pausar()
        self.m.reproducir(self.b)
        self.m.control.avanzar(70)
        self.m.control.pausar()
        self.assertEqual(self.m.historial.obtener("Dune").minuto, 10)
        self.assertEqual(self.m.historial.obtener("Interestelar").minuto, 70)
        self.assertEqual(self.m.historial.total(), 2)

    def test_04_un_titulo_sin_punto_empieza_en_cero(self):
        self.m.reproducir(self.b)
        self.assertEqual(self.m.control.minuto, 0)

    def test_05_el_memento_guardado_no_cambia_si_el_originador_sigue_avanzando(self):
        self.m.reproducir(self.a)
        self.m.control.avanzar(20)
        memento = self.m.control.crear_memento()
        self.m.control.avanzar(30)
        self.assertEqual(memento.minuto, 20)
        self.m.control.restaurar(memento)
        self.assertEqual(self.m.control.minuto, 20)

    def test_06_al_terminar_el_titulo_se_descarta_su_punto(self):
        self.m.reproducir(self.a)
        self.m.control.avanzar(40)
        self.m.control.pausar()
        self.m.reproducir(self.a)
        self.m.control.avanzar(100)
        self.assertIsNone(self.m.historial.obtener("Dune"))

    def test_07_el_historial_recuerda_el_ultimo_punto_guardado(self):
        h = HistorialPuntos()
        self.assertIsNone(h.ultimo())
        h.guardar("Dune", MementoReproduccion(self.a, 5))
        h.guardar("Interestelar", MementoReproduccion(self.b, 9))
        self.assertEqual(h.ultimo().minuto, 9)
        h.descartar("Interestelar")
        self.assertEqual(h.ultimo().minuto, 5)


if __name__ == "__main__":
    unittest.main()
