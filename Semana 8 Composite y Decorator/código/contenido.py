"""Patron Factory Method - Productos de contenido audiovisual."""

from abc import ABC, abstractmethod


class Contenido(ABC):
    """Interfaz comun para el contenido audiovisual del catalogo."""

    def __init__(self, titulo, duracion_minutos):
        self.titulo = titulo
        self.duracion_minutos = duracion_minutos

    @abstractmethod
    def reproducir(self):
        raise NotImplementedError

    def obtener_informacion(self):
        return f"{self.titulo} ({self.duracion_minutos} min) - {self.tipo}"


class Pelicula(Contenido):
    tipo = "Pelicula"

    def reproducir(self):
        return f"Reproduciendo la pelicula '{self.titulo}' en una sola sesion continua."


class Serie(Contenido):
    tipo = "Serie"

    def __init__(self, titulo, duracion_minutos, numero_episodios):
        super().__init__(titulo, duracion_minutos)
        self.numero_episodios = numero_episodios

    def reproducir(self):
        return (f"Reproduciendo el primer episodio de la serie '{self.titulo}' "
                f"(total de episodios: {self.numero_episodios}).")
