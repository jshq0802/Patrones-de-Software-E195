from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True)
class Novedad:
    titulo: str
    tipo: str
    genero: str


class Observador(ABC):
    @abstractmethod
    def actualizar(self, novedad: Novedad):
        raise NotImplementedError


class Sujeto(ABC):
    @abstractmethod
    def suscribir(self, observador: Observador):
        raise NotImplementedError

    @abstractmethod
    def desuscribir(self, observador: Observador):
        raise NotImplementedError

    @abstractmethod
    def notificar(self, novedad: Novedad):
        raise NotImplementedError


class CanalNovedades(Sujeto):
    """Sujeto concreto: mantiene la lista de observadores y los avisa."""

    def __init__(self):
        self._observadores = []

    def suscribir(self, observador: Observador):
        if observador not in self._observadores:
            self._observadores.append(observador)

    def desuscribir(self, observador: Observador):
        if observador in self._observadores:
            self._observadores.remove(observador)

    def total_observadores(self) -> int:
        return len(self._observadores)

    def notificar(self, novedad: Novedad):
        for observador in list(self._observadores):
            observador.actualizar(novedad)

    def publicar(self, novedad: Novedad):
        self.notificar(novedad)


class SuscriptorUsuario(Observador):
    """Observador: bandeja de un perfil, con filtro opcional por generos."""

    def __init__(self, nombre: str, generos=None):
        self.nombre = nombre
        self.generos = set(generos) if generos else None
        self.bandeja = []
        self._leidas = 0

    def actualizar(self, novedad: Novedad):
        if self.generos is None or novedad.genero in self.generos:
            self.bandeja.append(novedad)

    def no_leidas(self) -> int:
        return len(self.bandeja) - self._leidas

    def marcar_leidas(self):
        self._leidas = len(self.bandeja)


class RegistroNovedades(Observador):
    """Otro observador: guarda todo lo que se publica, sin filtrar."""

    def __init__(self):
        self.eventos = []

    def actualizar(self, novedad: Novedad):
        self.eventos.append(f"{novedad.tipo} nueva: {novedad.titulo} ({novedad.genero})")
