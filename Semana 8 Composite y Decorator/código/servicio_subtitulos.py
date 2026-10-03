from abc import ABC, abstractmethod


class ServicioSubtitulos(ABC):
    """Interfaz esperada por la plataforma (Target)."""

    @abstractmethod
    def obtener_subtitulos(self, codigo_idioma):
        raise NotImplementedError


class ProveedorSubtitulosExterno:
    """Servicio externo con una interfaz incompatible (Adaptee)."""

    def fetch_captions(self, lang_code):
        return {
            "lang": lang_code,
            "lines": [
                f"Linea de subtitulo 1 [{lang_code}]",
                f"Linea de subtitulo 2 [{lang_code}]",
            ],
        }


class AdaptadorProveedorSubtitulos(ServicioSubtitulos):
    """Adapter: traduce la interfaz del proveedor externo a ServicioSubtitulos."""

    def __init__(self, proveedor_externo: ProveedorSubtitulosExterno):
        self._proveedor_externo = proveedor_externo

    def obtener_subtitulos(self, codigo_idioma):
        respuesta = self._proveedor_externo.fetch_captions(codigo_idioma)
        return respuesta["lines"]
