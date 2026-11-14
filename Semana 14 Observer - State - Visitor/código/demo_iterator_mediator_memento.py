from facade_streaming import FachadaStreaming

fachada = FachadaStreaming(region="LATAM")
dune = fachada.publicar_pelicula("Dune", 100)
dark = fachada.publicar_serie("Dark", 60, numero_episodios=26)
crown = fachada.publicar_serie("The Crown", 58, numero_episodios=60)
lista = fachada.crear_lista_reproduccion("Maraton", [dune, dark, crown])

print("--- Iterator: recorrer la lista ---")
print("Todos:", [c.titulo for c in fachada.crear_iterador(lista)])
print("Solo series:", [c.titulo for c in fachada.crear_iterador(lista, "Serie")])

print("\n--- Mediator + Memento: reproducir, pausar y continuar ---")
m = fachada.crear_mediador_reproduccion(lista)
m.subtitulos.establecer_idioma("es")
m.reproducir(m.cola.siguiente())
m.control.avanzar(40)
m.cola.solicitar_siguiente()        # pasa a Dark y guarda el punto de Dune
m.control.avanzar(60)               # Dark termina y la cola entrega The Crown
m.reproducir(dune.contenido_base)   # Dune continua en el minuto 40
for linea in m.registro.eventos:
    print(" ", linea)
