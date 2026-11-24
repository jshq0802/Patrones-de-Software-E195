from abc import ABC, abstractmethod


class EstrategiaOrden(ABC):
    nombre = ""

    @abstractmethod
    def ordenar(self, fichas):
        raise NotImplementedError


class OrdenAlfabetico(EstrategiaOrden):
    nombre = "Titulo (A-Z)"

    def ordenar(self, fichas):
        return sorted(fichas, key=lambda f: f.contenido_base.titulo.lower())


class OrdenDuracionCorta(EstrategiaOrden):
    nombre = "Duracion (menor a mayor)"

    def ordenar(self, fichas):
        return sorted(fichas, key=lambda f: f.contenido_base.duracion_minutos)


class OrdenDuracionLarga(EstrategiaOrden):
    nombre = "Duracion (mayor a menor)"

    def ordenar(self, fichas):
        return sorted(fichas, key=lambda f: f.contenido_base.duracion_minutos, reverse=True)


class OrdenPorGenero(EstrategiaOrden):
    nombre = "Genero"

    def ordenar(self, fichas):
        return sorted(fichas, key=lambda f: ((f.genero or "").lower(), f.contenido_base.titulo.lower()))


class OrdenOriginal(EstrategiaOrden):
    nombre = "Orden de llegada"

    def ordenar(self, fichas):
        return list(fichas)


class OrganizadorCatalogo:

    def __init__(self, estrategia: EstrategiaOrden):
        self._estrategia = estrategia

    def cambiar_estrategia(self, estrategia: EstrategiaOrden):
        self._estrategia = estrategia

    def estrategia_actual(self):
        return self._estrategia

    def organizar(self, fichas):
        return self._estrategia.ordenar(fichas)


ESTRATEGIAS_DISPONIBLES = [OrdenOriginal, OrdenAlfabetico, OrdenDuracionCorta, OrdenDuracionLarga, OrdenPorGenero]
