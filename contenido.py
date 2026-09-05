"""
Modulo: contenido.py
Patron: FACTORY METHOD (creacional)
Proyecto: Plataforma de Streaming de Video
Semana: 2

Proposito
---------
Definir el "Producto" del patron Factory Method: la interfaz Contenido
y sus implementaciones concretas (Pelicula, Serie). Esta interfaz
permite que el modulo de Gestion de Contenido trabaje con distintos
tipos de contenido audiovisual sin depender de sus clases concretas,
cumpliendo con el principio de inversion de dependencias (DIP).
"""

from abc import ABC, abstractmethod


class Contenido(ABC):
    """Interfaz comun para todo el contenido audiovisual del catalogo."""

    def __init__(self, titulo, duracion_minutos):
        self.titulo = titulo
        self.duracion_minutos = duracion_minutos

    @abstractmethod
    def reproducir(self):
        """Logica de reproduccion especifica de cada tipo de contenido."""
        raise NotImplementedError

    def obtener_informacion(self):
        return f"{self.titulo} ({self.duracion_minutos} min) - {self.tipo}"


class Pelicula(Contenido):
    """Producto concreto: contenido de tipo pelicula."""

    tipo = "Pelicula"

    def reproducir(self):
        return f"Reproduciendo la pelicula '{self.titulo}' en una sola sesion continua."


class Serie(Contenido):
    """Producto concreto: contenido de tipo serie (organizada por episodios)."""

    tipo = "Serie"

    def __init__(self, titulo, duracion_minutos, numero_episodios):
        super().__init__(titulo, duracion_minutos)
        self.numero_episodios = numero_episodios

    def reproducir(self):
        return (f"Reproduciendo el primer episodio de la serie '{self.titulo}' "
                f"(total de episodios: {self.numero_episodios}).")
