"""Patron Memento - Guardar y recuperar el punto de reproduccion.

El originador (ControlReproduccion) crea un memento con su estado. El memento
es inmutable. El cuidador (HistorialPuntos) lo guarda sin leer su contenido y
lo devuelve cuando se quiere continuar viendo desde donde se dejo.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class MementoReproduccion:
    """Memento: instantanea inmutable del estado de la reproduccion."""
    contenido: object
    minuto: int


class HistorialPuntos:
    """Caretaker: guarda un punto por titulo. No abre ni modifica los mementos."""

    def __init__(self):
        self._puntos = {}
        self._ultimo = None

    def guardar(self, clave: str, memento: MementoReproduccion):
        self._puntos[clave] = memento
        self._ultimo = clave

    def obtener(self, clave: str):
        return self._puntos.get(clave)

    def descartar(self, clave: str):
        self._puntos.pop(clave, None)
        if self._ultimo == clave:
            self._ultimo = next(reversed(self._puntos), None)

    def ultimo(self):
        return self._puntos.get(self._ultimo)

    def total(self) -> int:
        return len(self._puntos)
