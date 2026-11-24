import unittest

from servicio_subtitulos import (
    ServicioSubtitulos,
    ProveedorSubtitulosExterno,
    AdaptadorProveedorSubtitulos,
)


class TestAdapterServicioSubtitulos(unittest.TestCase):

    def setUp(self):
        self.adaptador = AdaptadorProveedorSubtitulos(ProveedorSubtitulosExterno())

    def test_01_adaptador_cumple_la_interfaz_servicio_subtitulos(self):
        self.assertIsInstance(self.adaptador, ServicioSubtitulos)

    def test_02_adaptador_devuelve_una_lista_de_lineas(self):
        resultado = self.adaptador.obtener_subtitulos("es")
        self.assertIsInstance(resultado, list)
        self.assertEqual(len(resultado), 2)

    def test_03_adaptador_traduce_el_formato_del_proveedor_externo(self):
        resultado = self.adaptador.obtener_subtitulos("en")
        self.assertTrue(all("en" in linea for linea in resultado))

    def test_04_idiomas_distintos_devuelven_contenido_distinto(self):
        resultado_es = self.adaptador.obtener_subtitulos("es")
        resultado_en = self.adaptador.obtener_subtitulos("en")
        self.assertNotEqual(resultado_es, resultado_en)

    def test_05_cliente_funciona_con_la_abstraccion_sin_conocer_el_proveedor(self):
        def obtener_primera_linea(servicio: ServicioSubtitulos, idioma):
            return servicio.obtener_subtitulos(idioma)[0]

        primera_linea = obtener_primera_linea(self.adaptador, "pt")
        self.assertIn("pt", primera_linea)

    def test_06_proveedor_externo_conserva_su_interfaz_original(self):
        proveedor = ProveedorSubtitulosExterno()
        respuesta = proveedor.fetch_captions("fr")
        self.assertEqual(respuesta["lang"], "fr")
        self.assertIn("lines", respuesta)


if __name__ == "__main__":
    unittest.main(verbosity=2)
