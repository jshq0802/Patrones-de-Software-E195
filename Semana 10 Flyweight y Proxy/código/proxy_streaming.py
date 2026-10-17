from abc import ABC, abstractmethod


class AccesoDenegado(Exception):


class Usuario:
    def __init__(self, nombre, edad, suscripcion_activa=True):
        self.nombre = nombre
        self.edad = edad
        self.suscripcion_activa = suscripcion_activa


def edad_minima_de(clasificacion):
    if not clasificacion:
        return 0
    if clasificacion.startswith("PG-13"):
        return 13
    if clasificacion.startswith("R"):
        return 17
    return 0


class ServicioReproduccionRemota(ABC):

    @abstractmethod
    def transmitir(self, titulo):
        raise NotImplementedError


class ServidorStreamingReal(ServicioReproduccionRemota):

    instancias_creadas = 0

    def __init__(self):
        ServidorStreamingReal.instancias_creadas += 1
        self.manifiestos_descargados = 0

    def descargar_manifiesto(self, titulo):
        self.manifiestos_descargados += 1
        return f"manifiesto:{titulo}"

    def transmitir(self, titulo):
        manifiesto = self.descargar_manifiesto(titulo)
        return f"Transmitiendo '{titulo}' desde el servidor ({manifiesto})."


class ProxyServidorStreaming(ServicioReproduccionRemota):

    def __init__(self, usuario: Usuario):
        self._usuario = usuario
        self._servidor = None
        self._cache = {}
        self.registro_accesos = []
        self.aciertos_cache = 0

    def _validar(self, titulo, edad_minima):
        if not self._usuario.suscripcion_activa:
            self.registro_accesos.append(f"DENEGADO (sin suscripcion): {self._usuario.nombre} -> {titulo}")
            raise AccesoDenegado("La suscripcion no esta activa.")
        if self._usuario.edad < edad_minima:
            self.registro_accesos.append(f"DENEGADO (edad): {self._usuario.nombre} -> {titulo}")
            raise AccesoDenegado(f"Contenido para mayores de {edad_minima} anios.")

    def transmitir(self, titulo, edad_minima=0):
        self._validar(titulo, edad_minima)
        if titulo in self._cache:
            self.aciertos_cache += 1
            self.registro_accesos.append(f"CACHE: {self._usuario.nombre} -> {titulo}")
            return self._cache[titulo]
        if self._servidor is None:
            self._servidor = ServidorStreamingReal()
        resultado = self._servidor.transmitir(titulo)
        self._cache[titulo] = resultado
        self.registro_accesos.append(f"SERVIDOR: {self._usuario.nombre} -> {titulo}")
        return resultado

    @property
    def servidor_creado(self):
        return self._servidor is not None
