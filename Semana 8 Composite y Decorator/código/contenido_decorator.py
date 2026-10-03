

from contenido import Contenido


class ContenidoDecorator(Contenido):
    """Decorator base: envuelve un Contenido y delega en el, agregando comportamiento."""

    def __init__(self, contenido_envuelto: Contenido):
        self._contenido_envuelto = contenido_envuelto
        self.titulo = contenido_envuelto.titulo
        self.duracion_minutos = contenido_envuelto.duracion_minutos

    @property
    def tipo(self):
        return self._contenido_envuelto.tipo

    def reproducir(self):
        return self._contenido_envuelto.reproducir()

    def obtener_informacion(self):
        return self._contenido_envuelto.obtener_informacion()


class ConSubtitulos(ContenidoDecorator):
    def __init__(self, contenido_envuelto: Contenido, idioma: str):
        super().__init__(contenido_envuelto)
        self._idioma = idioma

    def reproducir(self):
        base = super().reproducir()
        return f"{base} [Subtitulos activados: {self._idioma}]"


class ConAudioDescriptivo(ContenidoDecorator):
    def reproducir(self):
        base = super().reproducir()
        return f"{base} [Audio descriptivo activado]"


class ConMarcaDeAgua(ContenidoDecorator):
    def __init__(self, contenido_envuelto: Contenido, texto: str):
        super().__init__(contenido_envuelto)
        self._texto = texto

    def reproducir(self):
        base = super().reproducir()
        return f"{base} [Marca de agua: {self._texto}]"
