from abc import ABC, abstractmethod


class MotorReproduccion(ABC):
    """Implementor."""

    @abstractmethod
    def iniciar_reproduccion(self, titulo, calidad):
        raise NotImplementedError


class MotorHTML5(MotorReproduccion):
    def iniciar_reproduccion(self, titulo, calidad):
        return f"[Motor HTML5] Reproduciendo '{titulo}' en calidad {calidad}."


class MotorNativo(MotorReproduccion):
    def iniciar_reproduccion(self, titulo, calidad):
        return f"[Motor nativo] Reproduciendo '{titulo}' en calidad {calidad}."


class Reproductor(ABC):
    """Abstraction."""

    def __init__(self, motor: MotorReproduccion):
        self._motor = motor

    @abstractmethod
    def reproducir_contenido(self, titulo, calidad):
        raise NotImplementedError


class ReproductorEstandar(Reproductor):
    def reproducir_contenido(self, titulo, calidad):
        return self._motor.iniciar_reproduccion(titulo, calidad)


class ReproductorPremium(Reproductor):
    def reproducir_contenido(self, titulo, calidad):
        resultado = self._motor.iniciar_reproduccion(titulo, calidad)
        return f"{resultado} Audio envolvente y HDR activados."
