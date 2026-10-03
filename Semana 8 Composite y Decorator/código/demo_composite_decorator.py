

from contenido import Pelicula, Serie
from lista_reproduccion import ContenidoHoja, ListaReproduccion
from contenido_decorator import ConSubtitulos, ConAudioDescriptivo, ConMarcaDeAgua

if __name__ == "__main__":
    print("\n=== Composite ===")
    pelicula = ContenidoHoja(Pelicula("Interestelar", 169))
    serie = ContenidoHoja(Serie("Breaking Bad", 47, numero_episodios=62))

    maraton = ListaReproduccion("Maraton de ciencia ficcion")
    maraton.agregar(pelicula)

    favoritos = ListaReproduccion("Mis favoritos")
    favoritos.agregar(maraton).agregar(serie)

    print(favoritos.mostrar())
    print("Duracion total:", favoritos.obtener_duracion_total(), "min")

    print("\n=== Decorator ===")
    base = Pelicula("Interestelar", 169)
    version_completa = ConMarcaDeAgua(ConAudioDescriptivo(ConSubtitulos(base, "es")), "StreamingX")
    print(version_completa.reproducir())
