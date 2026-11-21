from abc import ABC, abstractmethod


class Visitante(ABC):
    @abstractmethod
    def visitar_pelicula(self, pelicula):
        raise NotImplementedError

    @abstractmethod
    def visitar_serie(self, serie):
        raise NotImplementedError

    def visitar_lista(self, lista):
        for elemento in lista.obtener_elementos():
            elemento.aceptar(self)


class VisitanteReporte(Visitante):
    """Cuenta peliculas, series, episodios y minutos totales de contenido."""

    def __init__(self):
        self.peliculas = 0
        self.series = 0
        self.episodios = 0
        self.listas = 0
        self.minutos_totales = 0

    def visitar_pelicula(self, pelicula):
        self.peliculas += 1
        self.minutos_totales += pelicula.duracion_minutos

    def visitar_serie(self, serie):
        self.series += 1
        self.episodios += serie.numero_episodios
        self.minutos_totales += serie.duracion_minutos * serie.numero_episodios

    def visitar_lista(self, lista):
        self.listas += 1
        super().visitar_lista(lista)

    def horas_totales(self) -> float:
        return round(self.minutos_totales / 60, 1)

    def texto(self) -> str:
        return (f"Peliculas: {self.peliculas}\n"
                f"Series: {self.series} ({self.episodios} episodios)\n"
                f"Contenido total: {self.minutos_totales} min ({self.horas_totales()} horas)")


class VisitanteCostoLicencias(Visitante):
    """Calcula el costo de licencias: tarifa fija por pelicula y por episodio."""

    TARIFA_PELICULA = 12.0
    TARIFA_EPISODIO = 2.0

    def __init__(self):
        self.detalle = []
        self.total = 0.0

    def _registrar(self, titulo, costo):
        self.detalle.append((titulo, costo))
        self.total += costo

    def visitar_pelicula(self, pelicula):
        self._registrar(pelicula.titulo, self.TARIFA_PELICULA)

    def visitar_serie(self, serie):
        self._registrar(serie.titulo, self.TARIFA_EPISODIO * serie.numero_episodios)

    def texto(self) -> str:
        lineas = [f"{titulo}: USD {costo:.2f}" for titulo, costo in self.detalle]
        lineas.append(f"Total licencias: USD {self.total:.2f}")
        return "\n".join(lineas)
