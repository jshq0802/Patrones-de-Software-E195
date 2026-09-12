

class FichaContenido:
    """Producto: representa la ficha completa de un contenido del catalogo."""

    def __init__(self):
        self.contenido_base = None          # Objeto Contenido (Semana 2 - Factory Method)
        self.sinopsis = None
        self.genero = None
        self.clasificacion_audiencia = None
        self.anio_lanzamiento = None
        self.idiomas_disponibles = []
        self.subtitulos_disponibles = []
        self.reparto = []
        self.director_obra = None

    def __str__(self):
        info_base = self.contenido_base.obtener_informacion() if self.contenido_base else "Sin contenido base"
        return (
            f"Ficha de: {info_base}\n"
            f"  Genero: {self.genero or 'No especificado'}\n"
            f"  Clasificacion de audiencia: {self.clasificacion_audiencia or 'No especificada'}\n"
            f"  Anio de lanzamiento: {self.anio_lanzamiento or 'No especificado'}\n"
            f"  Sinopsis: {self.sinopsis or 'No especificada'}\n"
            f"  Idiomas disponibles: {', '.join(self.idiomas_disponibles) if self.idiomas_disponibles else 'No especificados'}\n"
            f"  Subtitulos disponibles: {', '.join(self.subtitulos_disponibles) if self.subtitulos_disponibles else 'No especificados'}\n"
            f"  Reparto: {', '.join(self.reparto) if self.reparto else 'No especificado'}\n"
            f"  Director/Creador: {self.director_obra or 'No especificado'}"
        )
