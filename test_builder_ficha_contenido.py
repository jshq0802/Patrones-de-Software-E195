
import unittest

from configuracion_global import ConfiguracionGlobal
from gestor_contenido_service import ServicioPeliculas, ServicioSeries
from ficha_contenido_builder import FichaContenidoBuilderEstandar, CatalogoDirector


class TestBuilderFichaContenido(unittest.TestCase):

    def setUp(self):
        # Se reinicia el Singleton de configuracion antes de cada prueba
        # para que los casos sean independientes entre si.
        ConfiguracionGlobal._reiniciar_para_pruebas()
        self.pelicula = ServicioPeliculas().crear_contenido("Interestelar", 169)
        self.serie = ServicioSeries().crear_contenido("Breaking Bad", 47, numero_episodios=62)

    def test_01_director_construye_ficha_basica_con_datos_minimos(self):
        """La ficha basica solo debe traer el contenido base establecido."""
        director = CatalogoDirector(FichaContenidoBuilderEstandar())
        ficha = director.construir_ficha_basica(self.pelicula)
        self.assertIs(ficha.contenido_base, self.pelicula)
        self.assertIsNone(ficha.sinopsis)
        self.assertIsNone(ficha.genero)

    def test_02_ficha_basica_usa_idioma_por_defecto_del_singleton(self):
        """
        Trazabilidad con la Semana 1: si no se especifican idiomas, el
        builder debe tomar el idioma por defecto de ConfiguracionGlobal.
        """
        ConfiguracionGlobal.obtener_instancia().establecer_parametro("idioma_por_defecto", "pt")
        director = CatalogoDirector(FichaContenidoBuilderEstandar())
        ficha = director.construir_ficha_basica(self.pelicula)
        self.assertEqual(ficha.idiomas_disponibles, ["pt"])

    def test_03_director_construye_ficha_completa_con_todos_los_datos(self):
        """La ficha completa debe contener toda la metadata proporcionada."""
        director = CatalogoDirector(FichaContenidoBuilderEstandar())
        ficha = director.construir_ficha_completa(
            contenido_base=self.serie,
            sinopsis="Sinopsis de prueba.",
            genero="Drama",
            clasificacion_audiencia="16+",
            anio_lanzamiento=2020,
            idiomas_disponibles=["es", "en"],
            subtitulos_disponibles=["es"],
            reparto=["Actor A", "Actor B"],
            director_obra="Directora X",
        )
        self.assertEqual(ficha.sinopsis, "Sinopsis de prueba.")
        self.assertEqual(ficha.genero, "Drama")
        self.assertEqual(ficha.clasificacion_audiencia, "16+")
        self.assertEqual(ficha.anio_lanzamiento, 2020)
        self.assertEqual(ficha.idiomas_disponibles, ["es", "en"])
        self.assertEqual(ficha.subtitulos_disponibles, ["es"])
        self.assertEqual(ficha.reparto, ["Actor A", "Actor B"])
        self.assertEqual(ficha.director_obra, "Directora X")

    def test_04_ficha_completa_conserva_contenido_base_de_factory_method(self):
        """
        Trazabilidad con la Semana 2: la ficha debe conservar el objeto
        Contenido (Pelicula/Serie) creado con Factory Method.
        """
        director = CatalogoDirector(FichaContenidoBuilderEstandar())
        ficha = director.construir_ficha_completa(
            contenido_base=self.serie,
            sinopsis="Sinopsis de prueba.",
            genero="Drama",
            clasificacion_audiencia="16+",
            anio_lanzamiento=2020,
            idiomas_disponibles=["es"],
            subtitulos_disponibles=["es"],
            reparto=["Actor A"],
            director_obra="Directora X",
        )
        self.assertIs(ficha.contenido_base, self.serie)
        self.assertEqual(ficha.contenido_base.numero_episodios, 62)

    def test_05_builder_permite_encadenamiento_de_metodos(self):
        """
        Cada paso del Concrete Builder debe devolver self, permitiendo
        el encadenamiento de metodos (estilo Fluent Builder).
        """
        builder = FichaContenidoBuilderEstandar()
        resultado = (
            builder
            .definir_contenido_base(self.pelicula)
            .definir_sinopsis_y_genero("Sinopsis", "Ciencia ficcion")
            .definir_clasificacion_y_anio("13+", 2014)
        )
        self.assertIs(resultado, builder)
        ficha = builder.obtener_ficha()
        self.assertEqual(ficha.genero, "Ciencia ficcion")

    def test_06_builders_independientes_no_comparten_estado(self):
        """Dos builders distintos deben producir fichas independientes."""
        builder_uno = FichaContenidoBuilderEstandar()
        builder_dos = FichaContenidoBuilderEstandar()

        builder_uno.definir_contenido_base(self.pelicula).definir_sinopsis_y_genero("A", "Genero A")
        builder_dos.definir_contenido_base(self.serie).definir_sinopsis_y_genero("B", "Genero B")

        ficha_uno = builder_uno.obtener_ficha()
        ficha_dos = builder_dos.obtener_ficha()

        self.assertNotEqual(ficha_uno.genero, ficha_dos.genero)
        self.assertIsNot(ficha_uno.contenido_base, ficha_dos.contenido_base)


if __name__ == "__main__":
    unittest.main(verbosity=2)
