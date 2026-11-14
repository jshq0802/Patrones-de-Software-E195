import unittest

from proxy_streaming import (ProxyServidorStreaming, ServidorStreamingReal, Usuario,
                             AccesoDenegado, edad_minima_de)


class TestProxyStreaming(unittest.TestCase):

    def setUp(self):
        ServidorStreamingReal.instancias_creadas = 0
        self.adulto = Usuario("ana", 30)
        self.menor = Usuario("tomas", 10)

    def test_01_el_servidor_real_no_se_crea_hasta_el_primer_uso(self):
        proxy = ProxyServidorStreaming(self.adulto)
        self.assertFalse(proxy.servidor_creado)
        self.assertEqual(ServidorStreamingReal.instancias_creadas, 0)
        proxy.transmitir("Dune")
        self.assertTrue(proxy.servidor_creado)
        self.assertEqual(ServidorStreamingReal.instancias_creadas, 1)

    def test_02_usuario_sin_suscripcion_es_rechazado(self):
        proxy = ProxyServidorStreaming(Usuario("sin_plan", 30, suscripcion_activa=False))
        with self.assertRaises(AccesoDenegado):
            proxy.transmitir("Dune")
        self.assertFalse(proxy.servidor_creado)

    def test_03_menor_de_edad_no_accede_a_contenido_restringido(self):
        proxy = ProxyServidorStreaming(self.menor)
        with self.assertRaises(AccesoDenegado):
            proxy.transmitir("Oppenheimer", edad_minima=13)

    def test_04_menor_si_accede_a_contenido_para_todo_publico(self):
        proxy = ProxyServidorStreaming(self.menor)
        self.assertIn("Transmitiendo", proxy.transmitir("Dark", edad_minima=0))

    def test_05_segunda_reproduccion_usa_la_cache_y_no_el_servidor(self):
        proxy = ProxyServidorStreaming(self.adulto)
        proxy.transmitir("Dune")
        proxy.transmitir("Dune")
        self.assertEqual(proxy.aciertos_cache, 1)
        self.assertEqual(proxy._servidor.manifiestos_descargados, 1)

    def test_06_el_registro_guarda_accesos_permitidos_y_denegados(self):
        proxy = ProxyServidorStreaming(self.menor)
        proxy.transmitir("Dark")
        with self.assertRaises(AccesoDenegado):
            proxy.transmitir("Oppenheimer", edad_minima=13)
        self.assertTrue(any(r.startswith("SERVIDOR") for r in proxy.registro_accesos))
        self.assertTrue(any(r.startswith("DENEGADO") for r in proxy.registro_accesos))

    def test_07_edad_minima_se_deduce_de_la_clasificacion(self):
        self.assertEqual(edad_minima_de("T (Todo publico) - Sistema RCC"), 0)
        self.assertEqual(edad_minima_de("PG-13 - Sistema MPAA"), 13)


if __name__ == "__main__":
    unittest.main()
