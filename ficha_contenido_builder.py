

from abc import ABC, abstractmethod

from ficha_contenido import FichaContenido
from configuracion_global import ConfiguracionGlobal


class FichaContenidoBuilder(ABC):
    """Interfaz Builder: define los pasos de construccion de una ficha."""

    @abstractmethod
    def definir_contenido_base(self, contenido_base):
        raise NotImplementedError

    @abstractmethod
    def definir_sinopsis_y_genero(self, sinopsis, genero):
        raise NotImplementedError

    @abstractmethod
    def definir_clasificacion_y_anio(self, clasificacion_audiencia, anio_lanzamiento):
        raise NotImplementedError

    @abstractmethod
    def definir_idiomas_y_subtitulos(self, idiomas_disponibles=None, subtitulos_disponibles=None):
        raise NotImplementedError

    @abstractmethod
    def definir_reparto(self, reparto=None, director_obra=None):
        raise NotImplementedError

    @abstractmethod
    def obtener_ficha(self):
        raise NotImplementedError


class FichaContenidoBuilderEstandar(FichaContenidoBuilder):
    """Concrete Builder: construye una FichaContenido paso a paso."""

    def __init__(self):
        self._ficha = FichaContenido()

    def definir_contenido_base(self, contenido_base):
        self._ficha.contenido_base = contenido_base
        return self

    def definir_sinopsis_y_genero(self, sinopsis, genero):
        self._ficha.sinopsis = sinopsis
        self._ficha.genero = genero
        return self

    def definir_clasificacion_y_anio(self, clasificacion_audiencia, anio_lanzamiento):
        self._ficha.clasificacion_audiencia = clasificacion_audiencia
        self._ficha.anio_lanzamiento = anio_lanzamiento
        return self

    def definir_idiomas_y_subtitulos(self, idiomas_disponibles=None, subtitulos_disponibles=None):
        if idiomas_disponibles:
            self._ficha.idiomas_disponibles = list(idiomas_disponibles)
        else:
            # Trazabilidad con la Semana 1 (Singleton): si no se indica
            # un idioma, se usa el idioma por defecto de la plataforma.
            idioma_por_defecto = ConfiguracionGlobal.obtener_instancia().obtener_parametro("idioma_por_defecto")
            self._ficha.idiomas_disponibles = [idioma_por_defecto]

        if subtitulos_disponibles:
            self._ficha.subtitulos_disponibles = list(subtitulos_disponibles)
        return self

    def definir_reparto(self, reparto=None, director_obra=None):
        if reparto:
            self._ficha.reparto = list(reparto)
        self._ficha.director_obra = director_obra
        return self

    def obtener_ficha(self):
        return self._ficha


class CatalogoDirector:
    """Director: orquesta el proceso de construccion de una ficha."""

    def __init__(self, builder: FichaContenidoBuilder):
        self._builder = builder

    def construir_ficha_basica(self, contenido_base):
        """Construye una ficha minima: solo el contenido base y el idioma por defecto."""
        self._builder.definir_contenido_base(contenido_base)
        self._builder.definir_idiomas_y_subtitulos()
        return self._builder.obtener_ficha()

    def construir_ficha_completa(self, contenido_base, sinopsis, genero,
                                  clasificacion_audiencia, anio_lanzamiento,
                                  idiomas_disponibles, subtitulos_disponibles,
                                  reparto, director_obra):
        """Construye una ficha con toda la metadata disponible."""
        self._builder.definir_contenido_base(contenido_base)
        self._builder.definir_sinopsis_y_genero(sinopsis, genero)
        self._builder.definir_clasificacion_y_anio(clasificacion_audiencia, anio_lanzamiento)
        self._builder.definir_idiomas_y_subtitulos(idiomas_disponibles, subtitulos_disponibles)
        self._builder.definir_reparto(reparto, director_obra)
        return self._builder.obtener_ficha()
