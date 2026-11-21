"""Patron Mediator - Coordinacion de los controles de reproduccion.

Los controles (reproduccion, subtitulos, cola y registro) no se conocen entre
si: cada uno solo avisa al mediador lo que le pasa, y el mediador decide que
hacen los demas. Aqui tambien se usan Iterator (la cola recorre la lista) y
Memento (el control guarda y recupera su punto).
"""

from abc import ABC, abstractmethod

from memento_reproduccion import MementoReproduccion, HistorialPuntos


class Mediador(ABC):
    @abstractmethod
    def notificar(self, emisor, evento: str):
        raise NotImplementedError


class Colega:
    def __init__(self):
        self._mediador = None

    def asignar_mediador(self, mediador: Mediador):
        self._mediador = mediador

    def _avisar(self, evento: str):
        if self._mediador is not None:
            self._mediador.notificar(self, evento)


class ControlReproduccion(Colega):
    """Colega y Originator del Memento: sabe que titulo suena y en que minuto."""

    def __init__(self):
        super().__init__()
        self.contenido = None
        self.minuto = 0
        self.reproduciendo = False

    def iniciar(self, contenido, minuto: int = 0):
        self.contenido = contenido
        self.minuto = minuto
        self.reproduciendo = True
        self._avisar("reproduciendo")

    def avanzar(self, minutos: int):
        if not self.reproduciendo:
            return
        self.minuto = min(self.minuto + minutos, self.contenido.duracion_minutos)
        if self.minuto >= self.contenido.duracion_minutos:
            self.reproduciendo = False
            self._avisar("terminado")

    def pausar(self):
        if not self.reproduciendo:
            return
        self.reproduciendo = False
        self._avisar("pausado")

    def crear_memento(self) -> MementoReproduccion:
        return MementoReproduccion(self.contenido, self.minuto)

    def restaurar(self, memento: MementoReproduccion):
        self.contenido = memento.contenido
        self.minuto = memento.minuto
        self.reproduciendo = False


class ControlSubtitulos(Colega):
    def __init__(self):
        super().__init__()
        self.idioma = None

    def establecer_idioma(self, idioma):
        self.idioma = idioma or None
        self._avisar("idioma_cambiado")

    def descripcion(self) -> str:
        return f"Subtitulos en {self.idioma}." if self.idioma else "Sin subtitulos."


class ColaReproduccion(Colega):
    """Colega que usa un Iterator para entregar el siguiente titulo."""

    def __init__(self):
        super().__init__()
        self._iterador = None

    def cargar(self, iterador):
        self._iterador = iterador

    def hay_siguiente(self) -> bool:
        return self._iterador is not None and self._iterador.hay_siguiente()

    def siguiente(self):
        return self._iterador.siguiente() if self.hay_siguiente() else None

    def solicitar_siguiente(self):
        self._avisar("siguiente_solicitado")


class RegistroActividad(Colega):
    def __init__(self):
        super().__init__()
        self.eventos = []

    def anotar(self, texto: str):
        self.eventos.append(texto)


class MediadorReproduccion(Mediador):
    """Mediator concreto: concentra las reglas de coordinacion."""

    def __init__(self, control, subtitulos, cola, registro, historial=None, autorizar=None):
        self._autorizar = autorizar
        self.control = control
        self.subtitulos = subtitulos
        self.cola = cola
        self.registro = registro
        self.historial = historial or HistorialPuntos()
        for colega in (control, subtitulos, cola, registro):
            colega.asignar_mediador(self)

    def reproducir(self, contenido, verificar=True) -> bool:
        """Inicia un titulo; si hay un punto guardado, continua desde ahi.
        Si hay una regla de autorizacion y la rechaza, no reproduce."""
        if verificar and self._autorizar is not None:
            permitido, motivo = self._autorizar(contenido)
            if not permitido:
                self.registro.anotar(f"Acceso denegado a '{contenido.titulo}': {motivo}")
                return False
        if self.control.reproduciendo:
            self.control.pausar()
        minuto = 0
        punto = self.historial.obtener(contenido.titulo)
        if punto is not None:
            self.control.restaurar(punto)
            minuto = self.control.minuto
            self.registro.anotar(f"Se recupero el punto guardado de '{contenido.titulo}'.")
        self.control.iniciar(contenido, minuto)
        return True

    def notificar(self, emisor, evento: str):
        titulo = self.control.contenido.titulo if self.control.contenido else ""
        if evento == "reproduciendo":
            self.registro.anotar(f"Reproduciendo '{titulo}' desde el minuto {self.control.minuto}.")
            self.registro.anotar(self.subtitulos.descripcion())
        elif evento == "pausado":
            self.historial.guardar(titulo, self.control.crear_memento())
            self.registro.anotar(f"Pausado en el minuto {self.control.minuto}. Punto guardado.")
        elif evento == "terminado":
            self.historial.descartar(titulo)
            self.registro.anotar(f"Termino '{titulo}'.")
            self._pasar_al_siguiente()
        elif evento == "siguiente_solicitado":
            self.control.pausar()
            self._pasar_al_siguiente()
        elif evento == "idioma_cambiado":
            self.registro.anotar(self.subtitulos.descripcion())

    def _pasar_al_siguiente(self):
        while True:
            siguiente = self.cola.siguiente()
            if siguiente is None:
                self.registro.anotar("Fin de la lista.")
                return
            if self.reproducir(siguiente):
                return
