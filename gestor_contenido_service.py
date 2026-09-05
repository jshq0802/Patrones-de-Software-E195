"""
Modulo: gestor_contenido_service.py
Patron: FACTORY METHOD (creacional)
Proyecto: Plataforma de Streaming de Video
Semana: 2

Proposito
---------
Definir el "Creator" del patron Factory Method: la clase abstracta
GestorContenidoService, que declara el metodo fabrica crear_contenido(),
y los creadores concretos (ServicioPeliculas, ServicioSeries), cada uno
responsable de instanciar el tipo de Contenido que le corresponde.

El metodo de negocio publicar_contenido() no necesita modificarse cada
vez que se agregue un nuevo tipo de contenido: solo se agrega un nuevo
creador concreto. Esto evita los condicionales que aparecerian en una
implementacion sin el patron (ver documento de la Semana 2).

Trazabilidad con la Semana 1
-----------------------------
Los creadores concretos consultan ConfiguracionGlobal (patron Singleton,
Semana 1) para aplicar la calidad maxima de reproduccion configurada
para toda la plataforma. Esto evidencia como los patrones implementados
en distintas semanas del proyecto colaboran entre si.
"""

from abc import ABC, abstractmethod

from contenido import Pelicula, Serie
from configuracion_global import ConfiguracionGlobal


class GestorContenidoService(ABC):
    """Creador abstracto: declara el metodo fabrica crear_contenido()."""

    @abstractmethod
    def crear_contenido(self, titulo, duracion_minutos, **kwargs):
        """Metodo fabrica: cada subclase decide que Contenido concreto crear."""
        raise NotImplementedError

    def publicar_contenido(self, titulo, duracion_minutos, **kwargs):
        """
        Metodo de negocio: usa el metodo fabrica para obtener el producto
        y aplica logica comun a todo tipo de contenido, como registrar la
        calidad maxima configurada (Singleton, Semana 1). Este metodo no
        cambia al incorporar nuevos tipos de contenido.
        """
        contenido = self.crear_contenido(titulo, duracion_minutos, **kwargs)
        calidad_maxima = ConfiguracionGlobal.obtener_instancia().obtener_parametro("calidad_maxima")
        return f"[Calidad configurada: {calidad_maxima}] {contenido.obtener_informacion()} publicado en el catalogo."


class ServicioPeliculas(GestorContenidoService):
    """Creador concreto: produce objetos Pelicula."""

    def crear_contenido(self, titulo, duracion_minutos, **kwargs):
        return Pelicula(titulo, duracion_minutos)


class ServicioSeries(GestorContenidoService):
    """Creador concreto: produce objetos Serie."""

    def crear_contenido(self, titulo, duracion_minutos, **kwargs):
        numero_episodios = kwargs.get("numero_episodios", 1)
        return Serie(titulo, duracion_minutos, numero_episodios)
