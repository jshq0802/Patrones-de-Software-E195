"""Patron Singleton - Configuracion global de la plataforma de streaming."""

import threading


class ConfiguracionGlobal:
    """Unica instancia de configuracion global del sistema."""

    _instancia = None
    _candado = threading.Lock()

    def __new__(cls):
        if cls._instancia is None:
            with cls._candado:
                if cls._instancia is None:
                    nueva_instancia = super().__new__(cls)
                    nueva_instancia._inicializado = False
                    cls._instancia = nueva_instancia
        return cls._instancia

    def __init__(self):
        if self._inicializado:
            return
        self._url_base_datos = "postgresql://localhost:5432/streaming_db"
        self._credenciales_servicios = {}
        self._parametros_sistema = {
            "calidad_maxima": "4K",
            "max_conexiones_simultaneas": 4,
            "idioma_por_defecto": "es",
        }
        self._inicializado = True

    @classmethod
    def obtener_instancia(cls):
        return cls()

    def obtener_url_base_datos(self):
        return self._url_base_datos

    def establecer_url_base_datos(self, url):
        self._url_base_datos = url

    def registrar_credencial(self, servicio, credencial):
        self._credenciales_servicios[servicio] = credencial

    def obtener_credencial(self, servicio):
        return self._credenciales_servicios.get(servicio)

    def establecer_parametro(self, clave, valor):
        self._parametros_sistema[clave] = valor

    def obtener_parametro(self, clave):
        return self._parametros_sistema.get(clave)

    @classmethod
    def _reiniciar_para_pruebas(cls):
        cls._instancia = None
