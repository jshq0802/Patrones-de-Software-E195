

from abc import ABC, abstractmethod

from iterador_lista import IteradorContenidos, IteradorPorTipo


class ElementoCatalogo(ABC):

    @abstractmethod
    def obtener_duracion_total(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def mostrar(self, nivel: int = 0) -> str:
        raise NotImplementedError

    @abstractmethod
    def aceptar(self, visitante):
        raise NotImplementedError

    def obtener_elementos(self):
        """Hijos directos. Una hoja no tiene hijos."""
        return ()

    def obtener_contenido(self):
        """Contenido que envuelve una hoja. Un compuesto no envuelve ninguno."""
        return None


class ContenidoHoja(ElementoCatalogo):

    def __init__(self, contenido):
        self._contenido = contenido

    def obtener_duracion_total(self) -> int:
        return self._contenido.duracion_minutos

    def obtener_contenido(self):
        return self._contenido

    def aceptar(self, visitante):
        return self._contenido.aceptar(visitante)

    def mostrar(self, nivel: int = 0) -> str:
        return ("  " * nivel) + f"- {self._contenido.obtener_informacion()}"


class ListaReproduccion(ElementoCatalogo):

    def __init__(self, nombre: str):
        self._nombre = nombre
        self._elementos = []

    def agregar(self, elemento: ElementoCatalogo):
        self._elementos.append(elemento)
        return self

    def quitar(self, elemento: ElementoCatalogo):
        self._elementos.remove(elemento)

    def obtener_duracion_total(self) -> int:
        return sum(e.obtener_duracion_total() for e in self._elementos)

    def mostrar(self, nivel: int = 0) -> str:
        lineas = [("  " * nivel) + f"+ {self._nombre} ({self.obtener_duracion_total()} min)"]
        for elemento in self._elementos:
            lineas.append(elemento.mostrar(nivel + 1))
        return "\n".join(lineas)

    def obtener_elementos(self):
        return tuple(self._elementos)

    def aceptar(self, visitante):
        return visitante.visitar_lista(self)

    def crear_iterador(self, tipo=None):
        """Iterator: recorre los contenidos sin exponer la estructura interna.
        Con tipo ('Pelicula' o 'Serie') entrega solo ese tipo."""
        if tipo is None:
            return IteradorContenidos(self)
        return IteradorPorTipo(self, tipo)

    def __iter__(self):
        return self.crear_iterador()
