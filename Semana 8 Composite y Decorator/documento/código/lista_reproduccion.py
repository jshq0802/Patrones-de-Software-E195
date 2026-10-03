

from abc import ABC, abstractmethod


class ElementoCatalogo(ABC):
    """Component: interfaz comun para contenido individual y listas de reproduccion."""

    @abstractmethod
    def obtener_duracion_total(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def mostrar(self, nivel: int = 0) -> str:
        raise NotImplementedError


class ContenidoHoja(ElementoCatalogo):
    """Leaf: envuelve un Contenido (Pelicula o Serie, Factory Method) como hoja del arbol."""

    def __init__(self, contenido):
        self._contenido = contenido

    def obtener_duracion_total(self) -> int:
        return self._contenido.duracion_minutos

    def mostrar(self, nivel: int = 0) -> str:
        return ("  " * nivel) + f"- {self._contenido.obtener_informacion()}"


class ListaReproduccion(ElementoCatalogo):
    """Composite: agrupa elementos hoja y otras listas de reproduccion anidadas."""

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
