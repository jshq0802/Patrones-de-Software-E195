from configuracion_global import ConfiguracionGlobal
from gestor_contenido_service import ServicioPeliculas, ServicioSeries
from configuracion_regional import FabricaConfiguracionLatam, FabricaConfiguracionUSA
from ficha_contenido_builder import FichaContenidoBuilderEstandar, CatalogoDirector
from servicio_subtitulos import ProveedorSubtitulosExterno, AdaptadorProveedorSubtitulos
from reproduccion_bridge import MotorHTML5, MotorNativo, ReproductorEstandar, ReproductorPremium
from lista_reproduccion import ListaReproduccion, ContenidoHoja
from contenido_decorator import ConSubtitulos, ConAudioDescriptivo, ConMarcaDeAgua


class FachadaStreaming:

    FABRICAS_REGIONALES = {
        "LATAM": FabricaConfiguracionLatam,
        "USA": FabricaConfiguracionUSA,
    }

    def __init__(self, region: str = "LATAM"):
        self._configuracion = ConfiguracionGlobal.obtener_instancia()
        self._servicio_peliculas = ServicioPeliculas()
        self._servicio_series = ServicioSeries()
        self._adaptador_subtitulos = AdaptadorProveedorSubtitulos(ProveedorSubtitulosExterno())
        self.establecer_region(region)

    def establecer_region(self, region: str):
        fabrica_cls = self.FABRICAS_REGIONALES.get(region, FabricaConfiguracionLatam)
        self._fabrica_regional = fabrica_cls()
        self._region = region
        return self._region

    def publicar_pelicula(self, titulo, duracion_minutos, sinopsis=None, genero=None):
        contenido = self._servicio_peliculas.crear_contenido(titulo, duracion_minutos)
        director = CatalogoDirector(FichaContenidoBuilderEstandar())
        return director.construir_ficha_regional(contenido, self._fabrica_regional, sinopsis, genero)

    def publicar_serie(self, titulo, duracion_minutos, numero_episodios, sinopsis=None, genero=None):
        contenido = self._servicio_series.crear_contenido(
            titulo, duracion_minutos, numero_episodios=numero_episodios
        )
        director = CatalogoDirector(FichaContenidoBuilderEstandar())
        return director.construir_ficha_regional(contenido, self._fabrica_regional, sinopsis, genero)

    def reproducir_ficha(self, ficha, premium=False, motor_html5=True):
        motor = MotorHTML5() if motor_html5 else MotorNativo()
        reproductor = ReproductorPremium(motor) if premium else ReproductorEstandar(motor)
        calidad = self._configuracion.obtener_parametro("calidad_maxima")
        return reproductor.reproducir_contenido(ficha.contenido_base.titulo, calidad)

    def obtener_subtitulos(self, codigo_idioma):
        return self._adaptador_subtitulos.obtener_subtitulos(codigo_idioma)

    def crear_lista_reproduccion(self, nombre, fichas):
        lista = ListaReproduccion(nombre)
        for ficha in fichas:
            lista.agregar(ContenidoHoja(ficha.contenido_base))
        return lista

    def mejorar_contenido(self, contenido, idioma_subtitulos=None,
                           audio_descriptivo=False, texto_marca_agua=None):
        resultado = contenido
        if idioma_subtitulos:
            resultado = ConSubtitulos(resultado, idioma_subtitulos)
        if audio_descriptivo:
            resultado = ConAudioDescriptivo(resultado)
        if texto_marca_agua:
            resultado = ConMarcaDeAgua(resultado, texto_marca_agua)
        return resultado

    def clonar_ficha_para_region(self, ficha, region):
        fabrica = self.FABRICAS_REGIONALES.get(region, FabricaConfiguracionLatam)()
        clon = ficha.clonar()
        clon.clasificacion_audiencia = fabrica.crear_politica_clasificacion().obtener_clasificacion_por_defecto()
        idiomas = fabrica.crear_configuracion_idiomas()
        clon.idiomas_disponibles = [idiomas.obtener_idioma_principal()] + idiomas.obtener_idiomas_secundarios()
        return clon
