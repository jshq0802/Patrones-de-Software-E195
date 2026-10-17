class PerfilCalidad:

    __slots__ = ("_nombre", "_resolucion", "_bitrate_kbps", "_codec")

    def __init__(self, nombre, resolucion, bitrate_kbps, codec):
        self._nombre = nombre
        self._resolucion = resolucion
        self._bitrate_kbps = bitrate_kbps
        self._codec = codec

    @property
    def nombre(self):
        return self._nombre

    @property
    def resolucion(self):
        return self._resolucion

    @property
    def bitrate_kbps(self):
        return self._bitrate_kbps

    @property
    def codec(self):
        return self._codec

    def describir(self, usuario, titulo, minuto):
        return (f"{usuario} ve '{titulo}' en el minuto {minuto} "
                f"[{self._nombre} - {self._resolucion} - {self._bitrate_kbps} kbps - {self._codec}]")


class FabricaPerfiles:

    _DEFINICIONES = {
        "720p": ("1280x720", 3000, "H.264"),
        "1080p": ("1920x1080", 6000, "H.264"),
        "4K": ("3840x2160", 16000, "H.265"),
    }

    def __init__(self):
        self._perfiles = {}

    def obtener(self, nombre):
        if nombre not in self._DEFINICIONES:
            raise ValueError(f"Calidad no soportada: {nombre}")
        if nombre not in self._perfiles:
            resolucion, bitrate, codec = self._DEFINICIONES[nombre]
            self._perfiles[nombre] = PerfilCalidad(nombre, resolucion, bitrate, codec)
        return self._perfiles[nombre]

    def total_perfiles_creados(self):
        return len(self._perfiles)


class SesionReproduccion:

    def __init__(self, usuario, titulo, minuto, perfil: PerfilCalidad):
        self.usuario = usuario
        self.titulo = titulo
        self.minuto = minuto
        self._perfil = perfil

    @property
    def perfil(self):
        return self._perfil

    def describir(self):
        return self._perfil.describir(self.usuario, self.titulo, self.minuto)
