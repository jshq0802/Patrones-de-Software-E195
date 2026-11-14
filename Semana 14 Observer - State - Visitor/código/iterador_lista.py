"""Patron Iterator - Recorrido de listas de reproduccion.

El Composite (ListaReproduccion) puede tener listas dentro de listas. El
iterador permite recorrer todos los contenidos, uno por uno, sin que el
cliente conozca como esta organizada la estructura por dentro. Se pueden
intercambiar distintos recorridos (todos, solo series, solo peliculas).
"""

from abc import ABC, abstractmethod


class Iterador(ABC):
    """Interfaz comun de todos los recorridos."""

    @abstractmethod
    def hay_siguiente(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def siguiente(self):
        raise NotImplementedError

    @abstractmethod
    def reiniciar(self):
        raise NotImplementedError

    def __iter__(self):
        return self

    def __next__(self):
        if not self.hay_siguiente():
            raise StopIteration
        return self.siguiente()


class IteradorContenidos(Iterador):
    """Recorre en profundidad una lista y entrega solo contenidos (las hojas),
    aplanando las listas anidadas. Es perezoso: no copia la estructura."""

    def __init__(self, raiz):
        self._raiz = raiz
        self.reiniciar()

    def _aceptar(self, contenido) -> bool:
        return True

    def reiniciar(self):
        self._pila = [iter(self._raiz.obtener_elementos())]
        self._avanzar()

    def _avanzar(self):
        self._pendiente = None
        while self._pila:
            try:
                elemento = next(self._pila[-1])
            except StopIteration:
                self._pila.pop()
                continue
            contenido = elemento.obtener_contenido()
            if contenido is None:
                self._pila.append(iter(elemento.obtener_elementos()))
            elif self._aceptar(contenido):
                self._pendiente = contenido
                return

    def hay_siguiente(self) -> bool:
        return self._pendiente is not None

    def siguiente(self):
        if self._pendiente is None:
            raise StopIteration
        actual = self._pendiente
        self._avanzar()
        return actual


class IteradorPorTipo(IteradorContenidos):
    """Mismo recorrido, pero solo entrega contenidos de un tipo."""

    def __init__(self, raiz, tipo: str):
        self._tipo = tipo
        super().__init__(raiz)

    def _aceptar(self, contenido) -> bool:
        return contenido.tipo == self._tipo
