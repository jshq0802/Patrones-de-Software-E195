"""Patron Factory Method - Creadores de contenido audiovisual."""

from abc import ABC, abstractmethod

from contenido import Pelicula, Serie
from configuracion_global import ConfiguracionGlobal


class GestorContenidoService(ABC):
    """Creador abstracto: declara el metodo fabrica crear_contenido()."""

    @abstractmethod
    def crear_contenido(self, titulo, duracion_minutos, **kwargs):
        raise NotImplementedError

    def publicar_contenido(self, titulo, duracion_minutos, **kwargs):
        contenido = self.crear_contenido(titulo, duracion_minutos, **kwargs)
        calidad_maxima = ConfiguracionGlobal.obtener_instancia().obtener_parametro("calidad_maxima")
        return f"[Calidad configurada: {calidad_maxima}] {contenido.obtener_informacion()} publicado en el catalogo."


class ServicioPeliculas(GestorContenidoService):
    def crear_contenido(self, titulo, duracion_minutos, **kwargs):
        return Pelicula(titulo, duracion_minutos)


class ServicioSeries(GestorContenidoService):
    def crear_contenido(self, titulo, duracion_minutos, **kwargs):
        numero_episodios = kwargs.get("numero_episodios", 1)
        return Serie(titulo, duracion_minutos, numero_episodios)
