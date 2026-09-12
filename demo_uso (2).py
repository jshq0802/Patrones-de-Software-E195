

from configuracion_global import ConfiguracionGlobal
from gestor_contenido_service import ServicioPeliculas, ServicioSeries
from ficha_contenido_builder import FichaContenidoBuilderEstandar, CatalogoDirector


class GestorUsuarios:
    def __init__(self):
        self.config = ConfiguracionGlobal.obtener_instancia()

    def conectar_bd(self):
        return f"GestorUsuarios conectando a: {self.config.obtener_url_base_datos()}"


class GestorReproduccion:
    def __init__(self):
        self.config = ConfiguracionGlobal.obtener_instancia()

    def calidad_por_defecto(self):
        return f"GestorReproduccion usando calidad: {self.config.obtener_parametro('calidad_maxima')}"


if __name__ == "__main__":
    # --- Semana 1: Singleton ---
    config = ConfiguracionGlobal.obtener_instancia()
    config.establecer_parametro("calidad_maxima", "1080p")
    config.registrar_credencial("servicio_drm", "clave-secreta-123")

    usuarios = GestorUsuarios()
    reproduccion = GestorReproduccion()

    print(usuarios.conectar_bd())
    print(reproduccion.calidad_por_defecto())
    print("Misma instancia en toda la app:",
          usuarios.config is reproduccion.config is config)

    print("-" * 60)

    # --- Semana 2: Factory Method ---
    servicio_peliculas = ServicioPeliculas()
    servicio_series = ServicioSeries()

    print(servicio_peliculas.publicar_contenido("El viaje del codigo", 118))
    print(servicio_series.publicar_contenido("Patrones en accion", 24, numero_episodios=8))

    pelicula = servicio_peliculas.crear_contenido("El viaje del codigo", 118)
    serie = servicio_series.crear_contenido("Patrones en accion", 24, numero_episodios=8)

    print(pelicula.reproducir())
    print(serie.reproducir())

    print("-" * 60)

    # --- Semana 3: Builder ---
    director_catalogo = CatalogoDirector(FichaContenidoBuilderEstandar())

    # Ficha basica: solo el contenido base y el idioma por defecto
    # tomado del Singleton de la Semana 1.
    ficha_basica = director_catalogo.construir_ficha_basica(pelicula)
    print(ficha_basica)

    print("-" * 60)

    # Ficha completa: toda la metadata disponible, reutilizando el
    # contenido de tipo Serie creado con Factory Method en la Semana 2.
    ficha_completa = director_catalogo.construir_ficha_completa(
        contenido_base=serie,
        sinopsis="Un grupo de desarrolladores enfrenta retos de diseño de software.",
        genero="Drama tecnologico",
        clasificacion_audiencia="13+",
        anio_lanzamiento=2024,
        idiomas_disponibles=["es", "en"],
        subtitulos_disponibles=["es", "en", "pt"],
        reparto=["Actor Uno", "Actor Dos"],
        director_obra="Directora Ejemplo",
    )
    print(ficha_completa)
