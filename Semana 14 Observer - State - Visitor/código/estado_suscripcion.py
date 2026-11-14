from abc import ABC, abstractmethod

ORDEN_CALIDAD = ["720p", "1080p", "4K"]


def limitar_calidad(calidad_global: str, calidad_plan: str) -> str:
    """Devuelve la menor de las dos calidades."""
    return min(calidad_global, calidad_plan, key=ORDEN_CALIDAD.index)


class ErrorSuscripcion(Exception):
    """Se lanza cuando el estado actual no permite la operacion."""


class EstadoSuscripcion(ABC):
    nombre = ""
    puede_reproducir = False
    calidad_maxima = None

    def pagar(self, suscripcion):
        self._no_permitido("pagar")

    def vencer(self, suscripcion):
        self._no_permitido("vencer")

    def cancelar(self, suscripcion):
        self._no_permitido("cancelar")

    def _no_permitido(self, operacion):
        raise ErrorSuscripcion(f"No se puede {operacion} una suscripcion en estado {self.nombre}.")


class EstadoPrueba(EstadoSuscripcion):
    nombre = "Prueba gratuita"
    puede_reproducir = True
    calidad_maxima = "720p"

    def pagar(self, suscripcion):
        suscripcion._cambiar_a(EstadoActiva())

    def vencer(self, suscripcion):
        suscripcion._cambiar_a(EstadoSuspendida())

    def cancelar(self, suscripcion):
        suscripcion._cambiar_a(EstadoCancelada())


class EstadoActiva(EstadoSuscripcion):
    nombre = "Activa"
    puede_reproducir = True
    calidad_maxima = "4K"

    def vencer(self, suscripcion):
        suscripcion._cambiar_a(EstadoSuspendida())

    def cancelar(self, suscripcion):
        suscripcion._cambiar_a(EstadoCancelada())


class EstadoSuspendida(EstadoSuscripcion):
    nombre = "Suspendida"

    def pagar(self, suscripcion):
        suscripcion._cambiar_a(EstadoActiva())

    def cancelar(self, suscripcion):
        suscripcion._cambiar_a(EstadoCancelada())


class EstadoCancelada(EstadoSuscripcion):
    nombre = "Cancelada"

    def pagar(self, suscripcion):
        suscripcion._cambiar_a(EstadoActiva())


class Suscripcion:
    """Contexto: delega en el estado actual y registra los cambios."""

    def __init__(self, estado: EstadoSuscripcion = None):
        self._estado = estado or EstadoPrueba()
        self.historial = [f"Inicio: {self._estado.nombre}"]

    @property
    def estado(self) -> str:
        return self._estado.nombre

    @property
    def puede_reproducir(self) -> bool:
        return self._estado.puede_reproducir

    @property
    def calidad_maxima(self):
        return self._estado.calidad_maxima

    def pagar(self):
        self._estado.pagar(self)

    def vencer(self):
        self._estado.vencer(self)

    def cancelar(self):
        self._estado.cancelar(self)

    def _cambiar_a(self, nuevo: EstadoSuscripcion):
        self.historial.append(f"{self._estado.nombre} -> {nuevo.nombre}")
        self._estado = nuevo

    def establecer_estado(self, nuevo: EstadoSuscripcion):
        self._estado = nuevo
        self.historial = [f"Inicio: {nuevo.nombre}"]

    def describir(self) -> str:
        calidad = self.calidad_maxima or "sin reproduccion"
        return f"{self.estado} ({calidad})"
