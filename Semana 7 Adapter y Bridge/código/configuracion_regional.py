"""Patron Abstract Factory - Familias de configuracion regional."""

from abc import ABC, abstractmethod


class PoliticaClasificacion(ABC):
    @abstractmethod
    def obtener_clasificacion_por_defecto(self):
        raise NotImplementedError


class ConfiguracionIdiomas(ABC):
    @abstractmethod
    def obtener_idioma_principal(self):
        raise NotImplementedError

    @abstractmethod
    def obtener_idiomas_secundarios(self):
        raise NotImplementedError


class PoliticaClasificacionLatam(PoliticaClasificacion):
    def obtener_clasificacion_por_defecto(self):
        return "T (Todo publico) - Sistema RCC"


class ConfiguracionIdiomasLatam(ConfiguracionIdiomas):
    def obtener_idioma_principal(self):
        return "es"

    def obtener_idiomas_secundarios(self):
        return ["en", "pt"]


class PoliticaClasificacionUSA(PoliticaClasificacion):
    def obtener_clasificacion_por_defecto(self):
        return "PG-13 - Sistema MPAA"


class ConfiguracionIdiomasUSA(ConfiguracionIdiomas):
    def obtener_idioma_principal(self):
        return "en"

    def obtener_idiomas_secundarios(self):
        return ["es"]


class FabricaConfiguracionRegional(ABC):
    """Fabrica abstracta: crea familias de objetos de configuracion regional."""

    @abstractmethod
    def crear_politica_clasificacion(self):
        raise NotImplementedError

    @abstractmethod
    def crear_configuracion_idiomas(self):
        raise NotImplementedError


class FabricaConfiguracionLatam(FabricaConfiguracionRegional):
    def crear_politica_clasificacion(self):
        return PoliticaClasificacionLatam()

    def crear_configuracion_idiomas(self):
        return ConfiguracionIdiomasLatam()


class FabricaConfiguracionUSA(FabricaConfiguracionRegional):
    def crear_politica_clasificacion(self):
        return PoliticaClasificacionUSA()

    def crear_configuracion_idiomas(self):
        return ConfiguracionIdiomasUSA()
