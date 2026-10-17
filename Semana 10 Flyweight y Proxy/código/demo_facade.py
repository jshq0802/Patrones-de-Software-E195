from facade_streaming import FachadaStreaming

if __name__ == "__main__":
    fachada = FachadaStreaming(region="LATAM")

    print("=== Publicar contenido (Factory Method + Abstract Factory + Builder) ===")
    pelicula = fachada.publicar_pelicula("Interestelar", 169, sinopsis="Viaje interestelar", genero="Ciencia ficcion")
    serie = fachada.publicar_serie("Dark", 60, numero_episodios=26, genero="Misterio")
    print(pelicula)
    print(serie)

    print("\n=== Reproducir (Bridge) ===")
    print(fachada.reproducir_ficha(pelicula, premium=False))
    print(fachada.reproducir_ficha(pelicula, premium=True))

    print("\n=== Subtitulos (Adapter) ===")
    print(fachada.obtener_subtitulos("es"))

    print("\n=== Lista de reproduccion (Composite) ===")
    lista = fachada.crear_lista_reproduccion("Maraton de la noche", [pelicula, serie])
    print(lista.mostrar())

    print("\n=== Contenido mejorado (Decorator) ===")
    mejorado = fachada.mejorar_contenido(
        pelicula.contenido_base, idioma_subtitulos="es",
        audio_descriptivo=True, texto_marca_agua="StreamingPlus",
    )
    print(mejorado.reproducir())

    print("\n=== Clonar ficha para otra region (Prototype + Abstract Factory) ===")
    pelicula_usa = fachada.clonar_ficha_para_region(pelicula, "USA")
    print("LATAM:", pelicula.clasificacion_audiencia, pelicula.idiomas_disponibles)
    print("USA:  ", pelicula_usa.clasificacion_audiencia, pelicula_usa.idiomas_disponibles)
