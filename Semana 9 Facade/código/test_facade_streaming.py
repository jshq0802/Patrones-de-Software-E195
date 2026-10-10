import unittest

from configuracion_global import ConfiguracionGlobal
from facade_streaming import FachadaStreaming


class TestFacadeStreaming(unittest.TestCase):

    def setUp(self):
        ConfiguracionGlobal._reiniciar_para_pruebas()
        self.fachada = FachadaStreaming(region="LATAM")

    def test_01_publicar_pelicula_aplica_politica_regional_latam(self):
        ficha = self.fachada.publicar_pelicula("Interestelar", 169)
        self.assertIn("RCC", ficha.clasificacion_audiencia)
        self.assertEqual(ficha.idiomas_disponibles[0], "es")

    def test_02_publicar_pelicula_region_usa_usa_otra_politica(self):
        self.fachada.establecer_region("USA")
        ficha = self.fachada.publicar_pelicula("Oppenheimer", 180)
        self.assertIn("MPAA", ficha.clasificacion_audiencia)
        self.assertEqual(ficha.idiomas_disponibles[0], "en")

    def test_03_publicar_serie_conserva_numero_de_episodios(self):
        ficha = self.fachada.publicar_serie("Dark", 60, numero_episodios=26)
        self.assertEqual(ficha.contenido_base.numero_episodios, 26)

    def test_04_reproducir_ficha_premium_agrega_mensaje_extra_del_bridge(self):
        ficha = self.fachada.publicar_pelicula("Dune", 155)
        mensaje_estandar = self.fachada.reproducir_ficha(ficha, premium=False)
        mensaje_premium = self.fachada.reproducir_ficha(ficha, premium=True)
        self.assertNotIn("HDR", mensaje_estandar)
        self.assertIn("HDR", mensaje_premium)

    def test_05_obtener_subtitulos_delega_en_el_adaptador(self):
        lineas = self.fachada.obtener_subtitulos("es")
        self.assertEqual(len(lineas), 2)
        self.assertIn("es", lineas[0])

    def test_06_crear_lista_reproduccion_suma_duraciones_de_varias_fichas(self):
        pelicula = self.fachada.publicar_pelicula("Dune", 155)
        serie = self.fachada.publicar_serie("Dark", 60, numero_episodios=26)
        lista = self.fachada.crear_lista_reproduccion("Maraton", [pelicula, serie])
        self.assertEqual(lista.obtener_duracion_total(), 215)

    def test_07_mejorar_contenido_apila_los_tres_decoradores(self):
        ficha = self.fachada.publicar_pelicula("Interestelar", 169)
        mejorado = self.fachada.mejorar_contenido(
            ficha.contenido_base,
            idioma_subtitulos="es",
            audio_descriptivo=True,
            texto_marca_agua="StreamingPlus",
        )
        resultado = mejorado.reproducir()
        self.assertIn("Subtitulos activados: es", resultado)
        self.assertIn("Audio descriptivo activado", resultado)
        self.assertIn("Marca de agua: StreamingPlus", resultado)

    def test_08_clonar_ficha_para_otra_region_no_reconstruye_el_contenido_base(self):
        ficha_latam = self.fachada.publicar_pelicula("Interestelar", 169)
        ficha_usa = self.fachada.clonar_ficha_para_region(ficha_latam, "USA")
        self.assertIs(ficha_usa.contenido_base, ficha_latam.contenido_base)
        self.assertNotEqual(ficha_usa.clasificacion_audiencia, ficha_latam.clasificacion_audiencia)
        self.assertEqual(ficha_usa.idiomas_disponibles[0], "en")
        self.assertEqual(ficha_latam.idiomas_disponibles[0], "es")


if __name__ == "__main__":
    unittest.main()
