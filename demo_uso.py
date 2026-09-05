"""
Modulo: demo_uso.py
Objetivo: mostrar como distintos modulos de la plataforma de streaming
usan los patrones implementados semana tras semana.

Semana 1 (Singleton): usuarios y reproduccion comparten la MISMA
configuracion global sin necesidad de recibirla como parametro ni de
crear su propia copia.

Semana 2 (Factory Method): el modulo de Gestion de Contenido crea
distintos tipos de contenido (Pelicula, Serie) a traves de creadores
concretos, sin que el codigo cliente dependa de las clases concretas.
"""

from configuracion_global import ConfiguracionGlobal
from gestor_contenido_service import ServicioPeliculas, ServicioSeries


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
