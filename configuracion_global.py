"""
Modulo: configuracion_global.py
Patron: SINGLETON (creacional)
Proyecto: Plataforma de Streaming de Video
Semana: 1

Proposito
---------
Garantizar que exista una unica instancia de la configuracion global
del sistema (URL de base de datos, credenciales de servicios externos
y parametros generales) y ofrecer un punto de acceso global y
controlado a dicha instancia, tal como lo define el patron Singleton
en Gamma, Helm, Johnson y Vlissides (GoF, 1994).

Version implementada
---------------------
Lazy Initialization + Double-Checked Locking (thread-safe), siguiendo
la recomendacion de evitar condiciones de carrera en entornos
multihilo (Bloch, "Effective Java", cap. sobre patrones Singleton).
"""

import threading


class ConfiguracionGlobal:
    """Unica instancia responsable de la configuracion global del sistema."""

    _instancia = None
    _candado = threading.Lock()

    def __new__(cls):
        # Primer chequeo (sin candado): evita adquirir el lock si la
        # instancia ya existe, mejorando el rendimiento.
        if cls._instancia is None:
            with cls._candado:
                # Segundo chequeo (dentro del candado): evita que dos
                # hilos creen la instancia al mismo tiempo.
                if cls._instancia is None:
                    nueva_instancia = super().__new__(cls)
                    nueva_instancia._inicializado = False
                    cls._instancia = nueva_instancia
        return cls._instancia

    def __init__(self):
        # __init__ se ejecuta cada vez que se llama ConfiguracionGlobal(),
        # incluso si __new__ devuelve la misma instancia. Este control
        # evita que el estado se reinicie en cada llamada.
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

    # ------------------------------------------------------------------
    # Punto de acceso global (equivalente a getInstance() en Java/GoF)
    # ------------------------------------------------------------------
    @classmethod
    def obtener_instancia(cls):
        """Punto de acceso global unico a la configuracion del sistema."""
        return cls()

    # ------------------------------------------------------------------
    # Operaciones sobre la configuracion (estado de la instancia unica)
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    # Uso exclusivo en pruebas unitarias: permite reiniciar el estado
    # del Singleton entre casos de prueba (no se usa en produccion).
    # ------------------------------------------------------------------
    @classmethod
    def _reiniciar_para_pruebas(cls):
        cls._instancia = None
