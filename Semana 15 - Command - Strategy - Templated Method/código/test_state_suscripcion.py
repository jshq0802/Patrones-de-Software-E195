import unittest

from estado_suscripcion import (Suscripcion, EstadoActiva, EstadoSuspendida, EstadoCancelada,
                                ErrorSuscripcion, limitar_calidad)
from proxy_streaming import Usuario, ProxyServidorStreaming, AccesoDenegado


class TestStateSuscripcion(unittest.TestCase):

    def test_01_la_suscripcion_nueva_empieza_en_prueba_con_720p(self):
        s = Suscripcion()
        self.assertEqual(s.estado, "Prueba gratuita")
        self.assertTrue(s.puede_reproducir)
        self.assertEqual(s.calidad_maxima, "720p")

    def test_02_pagar_en_prueba_pasa_a_activa_con_4k(self):
        s = Suscripcion()
        s.pagar()
        self.assertEqual(s.estado, "Activa")
        self.assertEqual(s.calidad_maxima, "4K")

    def test_03_vencer_una_activa_la_suspende_y_no_permite_reproducir(self):
        s = Suscripcion(EstadoActiva())
        s.vencer()
        self.assertEqual(s.estado, "Suspendida")
        self.assertFalse(s.puede_reproducir)

    def test_04_pagar_una_suspendida_la_reactiva(self):
        s = Suscripcion(EstadoSuspendida())
        s.pagar()
        self.assertEqual(s.estado, "Activa")

    def test_05_cancelada_solo_acepta_pagar(self):
        s = Suscripcion(EstadoCancelada())
        with self.assertRaises(ErrorSuscripcion):
            s.vencer()
        with self.assertRaises(ErrorSuscripcion):
            s.cancelar()
        s.pagar()
        self.assertEqual(s.estado, "Activa")

    def test_06_una_operacion_no_permitida_no_cambia_el_estado(self):
        s = Suscripcion(EstadoActiva())
        with self.assertRaises(ErrorSuscripcion):
            s.pagar()
        self.assertEqual(s.estado, "Activa")

    def test_07_el_historial_registra_cada_transicion(self):
        s = Suscripcion()
        s.pagar()
        s.vencer()
        self.assertEqual(s.historial, ["Inicio: Prueba gratuita",
                                       "Prueba gratuita -> Activa",
                                       "Activa -> Suspendida"])

    def test_08_el_proxy_respeta_el_estado_de_la_suscripcion(self):
        usuario = Usuario("Luis", 25, suscripcion=Suscripcion(EstadoSuspendida()))
        proxy = ProxyServidorStreaming(usuario)
        with self.assertRaises(AccesoDenegado):
            proxy.transmitir("Dune")
        usuario.suscripcion.pagar()
        self.assertIn("Transmitiendo", proxy.transmitir("Dune"))

    def test_09_la_calidad_real_es_la_menor_entre_el_ajuste_y_el_plan(self):
        self.assertEqual(limitar_calidad("4K", "720p"), "720p")
        self.assertEqual(limitar_calidad("1080p", "4K"), "1080p")

    def test_10_compatibilidad_usuario_con_bandera_booleana(self):
        self.assertTrue(Usuario("Ana", 30).suscripcion_activa)
        self.assertFalse(Usuario("Luis", 25, suscripcion_activa=False).suscripcion_activa)


if __name__ == "__main__":
    unittest.main()
