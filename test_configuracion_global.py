"""
Modulo: test_configuracion_global.py
Suite de pruebas unitarias para el patron Singleton (ConfiguracionGlobal).

Ejecucion:
    python -m unittest test_configuracion_global.py -v
"""

import threading
import unittest

from configuracion_global import ConfiguracionGlobal


class TestSingletonConfiguracionGlobal(unittest.TestCase):

    def setUp(self):
        # Se reinicia el Singleton antes de cada prueba para que los
        # casos sean independientes entre si.
        ConfiguracionGlobal._reiniciar_para_pruebas()

    def test_01_misma_instancia(self):
        """Dos llamadas deben devolver exactamente el mismo objeto."""
        instancia_a = ConfiguracionGlobal.obtener_instancia()
        instancia_b = ConfiguracionGlobal.obtener_instancia()
        self.assertIs(instancia_a, instancia_b)

    def test_02_valores_iniciales_por_defecto(self):
        """La instancia debe crearse con los valores por defecto esperados."""
        config = ConfiguracionGlobal.obtener_instancia()
        self.assertEqual(config.obtener_url_base_datos(),
                          "postgresql://localhost:5432/streaming_db")
        self.assertEqual(config.obtener_parametro("calidad_maxima"), "4K")

    def test_03_estado_compartido_entre_referencias(self):
        """Un cambio hecho desde una referencia debe verse desde otra."""
        instancia_a = ConfiguracionGlobal.obtener_instancia()
        instancia_a.establecer_url_base_datos("postgresql://prod:5432/streaming_db")

        instancia_b = ConfiguracionGlobal.obtener_instancia()
        self.assertEqual(instancia_b.obtener_url_base_datos(),
                          "postgresql://prod:5432/streaming_db")

    def test_04_registro_y_consulta_de_credenciales(self):
        config = ConfiguracionGlobal.obtener_instancia()
        config.registrar_credencial("servicio_drm", "clave-abc-123")
        self.assertEqual(config.obtener_credencial("servicio_drm"), "clave-abc-123")
        self.assertIsNone(config.obtener_credencial("servicio_inexistente"))

    def test_05_modificacion_de_parametros_persiste(self):
        config = ConfiguracionGlobal.obtener_instancia()
        config.establecer_parametro("max_conexiones_simultaneas", 8)
        nueva_referencia = ConfiguracionGlobal.obtener_instancia()
        self.assertEqual(nueva_referencia.obtener_parametro("max_conexiones_simultaneas"), 8)

    def test_06_no_se_reinicializa_en_llamadas_repetidas(self):
        """Aunque se llame varias veces, __init__ no debe borrar el estado."""
        config = ConfiguracionGlobal.obtener_instancia()
        config.establecer_parametro("idioma_por_defecto", "en")
        config_repetida = ConfiguracionGlobal.obtener_instancia()
        self.assertEqual(config_repetida.obtener_parametro("idioma_por_defecto"), "en")

    def test_07_thread_safety_una_sola_instancia_bajo_concurrencia(self):
        """
        Simula 50 hilos solicitando la instancia al mismo tiempo.
        Todas las instancias obtenidas deben ser el mismo objeto
        (valida el double-checked locking).
        """
        resultados = []

        def solicitar_instancia():
            resultados.append(ConfiguracionGlobal.obtener_instancia())

        hilos = [threading.Thread(target=solicitar_instancia) for _ in range(50)]
        for hilo in hilos:
            hilo.start()
        for hilo in hilos:
            hilo.join()

        primera = resultados[0]
        self.assertTrue(all(r is primera for r in resultados))
        self.assertEqual(len(set(id(r) for r in resultados)), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
