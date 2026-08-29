"""
Modulo: demo_uso.py
Objetivo: mostrar como distintos modulos futuros de la plataforma de
streaming (usuarios, catalogo, reproduccion) accederian a la MISMA
configuracion global sin necesidad de recibirla como parametro ni de
crear su propia copia.
"""

from configuracion_global import ConfiguracionGlobal


class GestorUsuarios:
    def __init__(self):
        self.config = ConfiguracionGlobal.obtener_instancia()

    def conectar_bd(self):
        return f"GestorUsuarios conectando a: {self.config.obtener_url_base_datos()}"


class GestorReproduccion:
    def __init__(self):
        self.config = ConfiguracionGlobal.obtener_instancia()

    def calidad_por_defecto(self):
        return f"GestorReproduccion usando calidad: {self.config.obtener_parametro('calidad_maxima')}"


if __name__ == "__main__":
    config = ConfiguracionGlobal.obtener_instancia()
    config.establecer_parametro("calidad_maxima", "1080p")
    config.registrar_credencial("servicio_drm", "clave-secreta-123")

    usuarios = GestorUsuarios()
    reproduccion = GestorReproduccion()

    print(usuarios.conectar_bd())
    print(reproduccion.calidad_por_defecto())
    print("Misma instancia en toda la app:",
          usuarios.config is reproduccion.config is config)
