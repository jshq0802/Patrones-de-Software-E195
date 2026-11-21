from facade_streaming import FachadaStreaming

fachada = FachadaStreaming()
fichas = [
    fachada.publicar_pelicula("Interestelar", 169, genero="Ciencia ficcion"),
    fachada.publicar_serie("Dark", 60, 26, genero="Misterio"),
    fachada.publicar_pelicula("Dune", 155, genero="Ciencia ficcion"),
]

print("== STRATEGY: el mismo catalogo con distintos criterios ==")
for criterio in fachada.criterios_de_orden():
    titulos = [f.contenido_base.titulo for f in fachada.ordenar_catalogo(fichas, criterio)]
    print(f"{criterio}: {titulos}")

print("\n== COMMAND: agregar, quitar y deshacer en Mi lista ==")
lista = fachada.crear_lista_reproduccion("Mi lista", [])
historial = fachada.crear_historial_comandos()
for ficha in fichas:
    fachada.agregar_a_lista(historial, lista, ficha)
fachada.quitar_de_lista(historial, lista, lista.elementos()[1])
print(lista.mostrar())
print("Deshacer ->", historial.deshacer())
print(lista.mostrar())
print("Rehacer ->", historial.rehacer())
print("Historial:", historial.registro())

print("\n== TEMPLATE METHOD: la misma lista en tres formatos ==")
for formato in fachada.formatos_exportacion():
    print(f"--- {formato} ---")
    print(fachada.exportar_lista(lista, formato))
